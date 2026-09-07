import numpy as np

from option_pricing.options import VanillaOption, BarrierOption


class MonteCarloPricer:
    def __init__(self, option: VanillaOption, seed: int | None = None):
        if option.exercise_style != "european":
            raise ValueError("Monte Carlo pricer only supports European options")

        self.option = option
        self.rng = np.random.default_rng(seed)

    def calculate_terminal_prices(self, num_simulations: int) -> np.ndarray:
        drift = (self.option.rate - 0.5 * self.option.volatility ** 2) * self.option.maturity
        vol = self.option.volatility * np.sqrt(self.option.maturity)

        z = self.rng.standard_normal(num_simulations)

        return self.option.spot * np.exp(drift + vol * z)

    def price(self, num_simulations: int) -> tuple[float, float]:
        terminal_prices = self.calculate_terminal_prices(num_simulations)

        if self.option.option_type == "call":
            payoff = np.maximum(terminal_prices - self.option.strike, 0)
        elif self.option.option_type == "put":
            payoff = np.maximum(self.option.strike - terminal_prices, 0)
        else:
            raise ValueError("option_type must be 'call' or 'put'")

        discounted_payoff = np.exp(-self.option.rate * self.option.maturity) * payoff

        price = discounted_payoff.mean()
        standard_error = discounted_payoff.std(ddof=1) / np.sqrt(num_simulations)

        return price, standard_error

    def price_antithetic(self, num_simulations: int) -> tuple[float, float]:
        if num_simulations % 2 == 1:
            num_simulations += 1

        num_pairs = num_simulations // 2

        drift = (self.option.rate - 0.5 * self.option.volatility ** 2) * self.option.maturity
        vol = self.option.volatility * np.sqrt(self.option.maturity)

        z = self.rng.standard_normal(num_pairs)

        terminal_prices_plus = self.option.spot * np.exp(drift + vol * z)
        terminal_prices_minus = self.option.spot * np.exp(drift - vol * z)

        if self.option.option_type == "call":
            payoff_plus = np.maximum(terminal_prices_plus - self.option.strike, 0)
            payoff_minus = np.maximum(terminal_prices_minus - self.option.strike, 0)
        elif self.option.option_type == "put":
            payoff_plus = np.maximum(self.option.strike - terminal_prices_plus, 0)
            payoff_minus = np.maximum(self.option.strike - terminal_prices_minus, 0)
        else:
            raise ValueError("option_type must be 'call' or 'put'")

        average_payoff = (payoff_plus + payoff_minus) / 2
        discounted_payoff = np.exp(-self.option.rate * self.option.maturity) * average_payoff
        price = discounted_payoff.mean()
        standard_error = discounted_payoff.std(ddof=1) / np.sqrt(num_pairs)

        return price, standard_error

    def generate_price_paths(self, num_simulations: int, num_steps: int) -> tuple[np.ndarray, np.ndarray]:
        dt = self.option.maturity / num_steps
        drift = (self.option.rate - 0.5 * self.option.volatility ** 2) * dt
        vol = self.option.volatility * np.sqrt(dt)

        paths = np.zeros((num_steps + 1, num_simulations))
        paths[0] = self.option.spot

        for t in range(1, num_steps + 1):
            z = self.rng.standard_normal(num_simulations)
            paths[t] = paths[t - 1] * np.exp(drift + vol * z)

        time = np.linspace(0, self.option.maturity, num_steps + 1)

        return paths, time


class BarrierMonteCarloPricer(MonteCarloPricer):
    def __init__(self, option: BarrierOption, seed: int | None = None):
        self.option = option
        self.rng = np.random.default_rng(seed)

    def up_and_out_call(self, num_simulations: int, num_steps: int) -> tuple[float, float]:
        paths, _ = self.generate_price_paths(num_simulations, num_steps)

        hit = (paths >= self.option.barrier).any(axis=0)
        terminal_prices = paths[-1]

        payoff = np.maximum(terminal_prices - self.option.strike, 0)
        payoff = np.where(hit, 0, payoff)

        discounted_payoff = np.exp(-self.option.rate * self.option.maturity) * payoff
        price = discounted_payoff.mean()
        standard_error = discounted_payoff.std(ddof=1) / np.sqrt(num_simulations)

        return price, standard_error
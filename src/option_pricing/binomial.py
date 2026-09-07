import numpy as np

from option_pricing.options import VanillaOption


class BinomialPricer:
    def __init__(self, option: VanillaOption, steps: int):
        self.option = option
        self.steps = steps

    def calculate_parameters(self) -> tuple[float, float, float, float]:
        dt = self.option.maturity / self.steps
        up = np.exp(self.option.volatility * np.sqrt(dt))
        down = 1 / up
        probability = (np.exp(self.option.rate * dt) - down) / (up - down)

        return dt, up, down, probability

    def calculate_stock_prices(self, step: int, up: float, down: float) -> np.ndarray:
        up_moves = np.arange(step + 1)
        down_moves = step - up_moves

        return self.option.spot * up ** up_moves * down ** down_moves

    def calculate_intrinsic_values(self, stock_prices: np.ndarray) -> np.ndarray:
        if self.option.option_type == "call":
            return np.maximum(stock_prices - self.option.strike, 0)
        elif self.option.option_type == "put":
            return np.maximum(self.option.strike - stock_prices, 0)
        else:
            raise ValueError("option_type must be 'call' or 'put'")

    def price(self) -> float:
        dt, up, down, probability = self.calculate_parameters()

        terminal_prices = self.calculate_stock_prices(self.steps, up, down)
        option_values = self.calculate_intrinsic_values(terminal_prices)

        discount = np.exp(-self.option.rate * dt)

        for step in range(self.steps - 1, -1, -1):
            continuation_values = discount * (probability * option_values[1:] + (1 - probability) * option_values[:-1])

            if self.option.exercise_style == "american":
                stock_prices = self.calculate_stock_prices(step, up, down)
                intrinsic_values = self.calculate_intrinsic_values(stock_prices)
                option_values = np.maximum(continuation_values, intrinsic_values)
            else:
                option_values = continuation_values

        return float(option_values[0])
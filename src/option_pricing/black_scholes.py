import numpy as np
from scipy.stats import norm

from option_pricing.options import VanillaOption


class BlackScholesPricer:
    def __init__(self, option: VanillaOption):
        if option.exercise_style != "european":
            raise ValueError("Black-Scholes pricer only supports European options")

        self.option = option

    def calculate_d1(self) -> float:
        num = np.log(self.option.spot / self.option.strike) + (
                    self.option.rate + 0.5 * self.option.volatility ** 2) * self.option.maturity
        den = self.option.volatility * np.sqrt(self.option.maturity)

        return num / den

    def calculate_d2(self, d1: float) -> float:
        return d1 - self.option.volatility * np.sqrt(self.option.maturity)

    def call_price(self) -> float:
        d1 = self.calculate_d1()
        d2 = self.calculate_d2(d1)

        return self.option.spot * norm.cdf(d1) - (
                    self.option.strike * np.exp(-self.option.rate * self.option.maturity) * norm.cdf(d2))

    def put_price(self) -> float:
        d1 = self.calculate_d1()
        d2 = self.calculate_d2(d1)

        return self.option.strike * np.exp(-self.option.rate * self.option.maturity) * norm.cdf(-d2) - (
                    self.option.spot * norm.cdf(-d1))

    def price(self) -> float:
        if self.option.option_type == "call":
            return self.call_price()
        elif self.option.option_type == "put":
            return self.put_price()
        else:
            raise ValueError("option_type must be 'call' or 'put'")
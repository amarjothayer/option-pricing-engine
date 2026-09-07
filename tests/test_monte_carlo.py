import pytest

from option_pricing.options import VanillaOption
from option_pricing.black_scholes import BlackScholesPricer
from option_pricing.monte_carlo import MonteCarloPricer


def test_monte_carlo_close_to_black_scholes():
    option = VanillaOption(
        spot=100,
        strike=100,
        maturity=1,
        rate=0.05,
        volatility=0.2,
        option_type="call",
    )

    monte_carlo_price, _ = MonteCarloPricer(option, seed=42).price(num_simulations=100000)
    black_scholes_price = BlackScholesPricer(option).price()

    assert monte_carlo_price == pytest.approx(black_scholes_price, abs=0.1)
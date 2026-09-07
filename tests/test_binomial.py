import pytest

from option_pricing.options import VanillaOption
from option_pricing.black_scholes import BlackScholesPricer
from option_pricing.binomial import BinomialPricer


def test_binomial_converges_to_black_scholes():
    option = VanillaOption(
        spot=100,
        strike=100,
        maturity=1,
        rate=0.05,
        volatility=0.2,
        option_type="call",
    )

    binomial_price = BinomialPricer(option, steps=1000).price()
    black_scholes_price = BlackScholesPricer(option).price()

    assert binomial_price == pytest.approx(black_scholes_price, abs=0.01)


def test_american_put_at_least_european_put():
    european_put = VanillaOption(
        spot=100,
        strike=100,
        maturity=1,
        rate=0.05,
        volatility=0.2,
        option_type="put",
        exercise_style="european",
    )

    american_put = VanillaOption(
        spot=100,
        strike=100,
        maturity=1,
        rate=0.05,
        volatility=0.2,
        option_type="put",
        exercise_style="american",
    )

    european_price = BinomialPricer(european_put, steps=500).price()
    american_price = BinomialPricer(american_put, steps=500).price()

    assert american_price >= european_price
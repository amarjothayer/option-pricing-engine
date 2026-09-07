import pytest

from option_pricing.options import VanillaOption
from option_pricing.black_scholes import BlackScholesPricer


def test_call_price():
    option = VanillaOption(
        spot=100,
        strike=100,
        maturity=1,
        rate=0.05,
        volatility=0.2,
        option_type="call",
    )

    pricer = BlackScholesPricer(option)

    assert pricer.price() == pytest.approx(10.4506, abs=1e-4)


def test_put_price():
    option = VanillaOption(
        spot=100,
        strike=100,
        maturity=1,
        rate=0.05,
        volatility=0.2,
        option_type="put",
    )

    pricer = BlackScholesPricer(option)

    assert pricer.price() == pytest.approx(5.5735, abs=1e-4)
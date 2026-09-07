from dataclasses import dataclass


@dataclass
class VanillaOption:
    spot: float
    strike: float
    maturity: float
    rate: float
    volatility: float
    option_type: str
    exercise_style: str = "european"


@dataclass
class BarrierOption:
    spot: float
    strike: float
    maturity: float
    rate: float
    volatility: float
    barrier: float
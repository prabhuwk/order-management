from enum import Enum


class Strike(Enum):
    BANKNIFTY = 100
    NIFTY = 50
    FINNIFTY = 50
    SENSEX = 100


class StrikePrice:
    def __init__(self, symbol_name: str, spot_price: float) -> None:
        self.symbol_name = symbol_name
        self.spot_price = spot_price

    @property
    def value(self):
        if Strike[self.symbol_name].value == 100:
            return round(self.spot_price / 100) * 100
        if Strike[self.symbol_name].value == 50:
            return round(self.spot_price / 50) * 50

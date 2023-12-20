from enum import Enum


class Strike(Enum):
    MIDCPNIFTY = 25
    BANKNIFTY = 100
    NIFTY = 50
    FINNIFTY = 50
    SENSEX = 100


class StrikePrice:
    def __init__(self, symbol_name: str, spot_price: float, option_type: str) -> None:
        self.symbol_name = symbol_name
        self.spot_price = spot_price
        self.option_type = option_type
        self.current = self._current()
        self.required = self._required()

    def _current(self):
        if Strike[self.symbol_name].value == 100:
            return round(self.spot_price / 100) * 100
        if Strike[self.symbol_name].value == 50:
            return round(self.spot_price / 50) * 50
        if Strike[self.symbol_name].value == 25:
            return round(self.spot_price / 25) * 25

    def _required(self):
        if Strike[self.symbol_name].value == 100:
            return (
                self.current - 100 if self.option_type == "PUT" else self.current + 100
            )
        if Strike[self.symbol_name].value == 50:
            return self.current - 50 if self.option_type == "PUT" else self.current + 50
        if Strike[self.symbol_name].value == 25:
            return self.current - 25 if self.option_type == "PUT" else self.current + 25

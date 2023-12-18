from enum import Enum

from contract import Contract
from strike_price import StrikePrice


class OptionType(Enum):
    BUY = "PUT"
    SELL = "CALL"


class ProcessOrder:
    def __init__(
        self,
        dhan_client,
        symbol_name: str,
        symbols_file_path: str,
        data: dict,
        signal: str,
    ) -> None:
        self.dhan_client = dhan_client
        self.symbol_name = symbol_name
        self.symbols_file_path = symbols_file_path
        self.spot_price = data.get("close")
        self.signal = signal
        self.security_id = self._security_id()
        self.strike_price = StrikePrice(self.symbol_name, self.spot_price)

    def _security_id(self):
        option_type = OptionType[self.signal].value
        required_strike_price = self.strike_price.required()
        contracts = Contract(
            symbol_name=self.symbol_name,
            strike_price=required_strike_price,
            type=option_type,
            symbols_file_path=self.symbols_file_path,
        )
        return contracts.id_

from typing import Dict, List, Literal, LiteralString

from dhanhq import dhanhq


class Positions:
    def __init__(self, dhan_client: dhanhq):
        self.dhan_client = dhan_client

    @property
    def get(self) -> List[Dict]:
        positions = self.dhan_client.get_positions()
        return positions.get("data") if positions.get("status") == "success" else None

    def exists(
        self,
        symbol_name: LiteralString,
        position_type: Literal["SHORT", "LONG", "CLOSED"],
    ) -> bool:
        for position in self.get:
            if position.get("positionType") == position_type:
                trading_symbol = position.get("tradingSymbol").split("-")[0]
                if trading_symbol == symbol_name:
                    return True
        return False

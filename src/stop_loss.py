from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Literal


class StopLossBuffer(Enum):
    MIDCPNIFTY = 5
    BANKNIFTY = 25
    NIFTY = 10
    FINNIFTY = 10
    SENSEX = 45


class StopLoss(ABC):
    def __init__(
        self,
        current_candle: Dict[str, List[float]],
        ordered_candle: Dict,
        symbol_name: str,
    ):
        self.current_candle = current_candle
        self.ordered_candle = ordered_candle
        self.symbol_name = symbol_name

    @property
    @abstractmethod
    def hit(self):
        pass


class BuyStopLoss(StopLoss):
    @property
    def hit(self) -> bool:
        return (
            self.current_candle["low"][-1] - StopLossBuffer[self.symbol_name].value
            < self.ordered_candle["low"]
        )


class SellStopLoss(StopLoss):
    @property
    def hit(self) -> bool:
        return (
            self.current_candle["high"][-1] + StopLossBuffer[self.symbol_name].value
            > self.ordered_candle["high"]
        )


class StopLossFactory:
    @staticmethod
    def get_stop_loss(
        signal: Literal["BUY", "SELL"],
        current_candle: Dict[str, List[float]],
        ordered_candle: Dict,
        symbol_name: str,
    ) -> StopLoss:
        if signal == "BUY":
            return BuyStopLoss(current_candle, ordered_candle, symbol_name)
        elif signal == "SELL":
            return SellStopLoss(current_candle, ordered_candle, symbol_name)

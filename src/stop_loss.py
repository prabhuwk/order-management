from abc import ABC, abstractmethod
from typing import Dict, List, Literal


class StopLoss(ABC):
    def __init__(self, current_candle: Dict[str, List[float]], ordered_candle: Dict):
        self.current_candle = current_candle
        self.ordered_candle = ordered_candle

    @abstractmethod
    def hit(self):
        pass


class BuyStopLoss(StopLoss):
    def hit(self) -> bool:
        return self.current_candle["low"][-1] < self.ordered_candle["low"]


class SellStopLoss(StopLoss):
    def hit(self) -> bool:
        return self.current_candle["high"][-1] > self.ordered_candle["high"]


class StopLossFactory:
    @staticmethod
    def get_stop_loss(
        signal: Literal["BUY", "SELL"],
        current_candle: Dict[str, List[float]],
        ordered_candle: Dict,
    ) -> StopLoss:
        if signal == "BUY":
            return BuyStopLoss(current_candle, ordered_candle)
        elif signal == "SELL":
            return SellStopLoss(current_candle, ordered_candle)

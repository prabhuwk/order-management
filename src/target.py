from abc import ABC, abstractmethod
from typing import Dict, List, Literal


class Target(ABC):
    def __init__(
        self,
        current_candle: Dict[str, List[float]],
        ordered_candle: Dict,
        percent: float,
    ):
        self.current_candle = current_candle
        self.ordered_candle = ordered_candle
        self.percent = percent

    @abstractmethod
    def price(self):
        pass

    @property
    @abstractmethod
    def hit(self):
        pass


class BuyTarget(Target):
    def price(self) -> float:
        return self.ordered_candle["support"] + (
            (self.ordered_candle["resistance"] - self.ordered_candle["support"])
            * (self.percent / 100)
        )

    @property
    def hit(self) -> bool:
        return self.current_candle["high"][-1] > self.price()


class SellTarget(Target):
    def price(self) -> float:
        return self.ordered_candle["support"] + (
            (self.ordered_candle["resistance"] - self.ordered_candle["support"])
            * ((100 - self.percent) / 100)
        )

    @property
    def hit(self) -> bool:
        return self.current_candle["low"][-1] > self.price()


class TargetFactory:
    @staticmethod
    def get_target(
        signal: Literal["BUY", "SELL"],
        current_candle: Dict[str, List[float]],
        ordered_candle: Dict,
        percent: float,
    ) -> Target:
        if signal == "BUY":
            return BuyTarget(current_candle, ordered_candle, percent)
        elif signal == "SELL":
            return SellTarget(current_candle, ordered_candle, percent)

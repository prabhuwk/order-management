import time
from typing import Literal

from minute_chart import MinuteChart
from order import Order
from stop_loss import StopLossFactory
from target import TargetFactory


def process_order(
    minute_chart: MinuteChart,
    order: Order,
    symbol_id: str,
    security_id: str,
    ordered_candle: dict,
    quantity: int,
    signal: Literal["BUY", "SELL"],
    target_percent: int,
):
    while True:
        current_candle = minute_chart.intraday(security_id=symbol_id)
        stop_loss = StopLossFactory.get_stop_loss(
            signal=signal,
            current_candle=current_candle,
            ordered_candle=ordered_candle,
        )
        target = TargetFactory.get_target(
            signal=signal,
            current_candle=current_candle,
            ordered_candle=ordered_candle,
            percent=target_percent,
        )
        if stop_loss.hit or target.hit:
            return order.buy(security_id=security_id, quantity=quantity)
        time.sleep(60)

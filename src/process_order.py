import time
from datetime import datetime
from typing import Literal

from minute_chart import MinuteChart
from order import Order
from positions import Positions
from stop_loss import StopLossFactory
from target import TargetFactory


def process_order(
    minute_chart: MinuteChart,
    order: Order,
    symbol_security_id: str,
    contract_security_id: str,
    ordered_candle: dict,
    quantity: int,
    signal: Literal["BUY", "SELL"],
    target_percent: int,
    positions: Positions,
    position_type: Literal["SHORT", "LONG", "CLOSED"],
):
    while True:
        current_candle = minute_chart.intraday(security_id=symbol_security_id)
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
        current_time = datetime.now()
        if (
            stop_loss.hit
            or target.hit
            or (current_time.hour == 15 and current_time.minute == 28)
        ):
            if positions.exists(
                security_id=contract_security_id, position_type=position_type
            ):
                return order.buy(security_id=contract_security_id, quantity=quantity)
            return
        time.sleep(60)

import logging
import time
from datetime import datetime
from typing import Literal

from minute_chart import MinuteChart
from order import Order
from positions import Positions
from stop_loss import StopLossFactory
from target import TargetFactory
from trading_hours import TradingHours

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


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
    symbol_name: str,
    trading_hours: TradingHours,
):
    while True:
        time.sleep(60)
        logger.info("get every minute candlestick data to check stop loss and target")
        current_candle = minute_chart.intraday(security_id=symbol_security_id)
        stop_loss = StopLossFactory.get_stop_loss(
            signal=signal,
            current_candle=current_candle,
            ordered_candle=ordered_candle,
            symbol_name=symbol_name,
        )
        target = TargetFactory.get_target(
            signal=signal,
            current_candle=current_candle,
            ordered_candle=ordered_candle,
            percent=target_percent,
        )
        current_time = datetime.now()
        logger.info(f"stop loss hit is {stop_loss.hit} and target hit is {target.hit}")
        if (
            stop_loss.hit
            or target.hit
            or (current_time.hour == 15 and current_time.minute == 28)
        ):
            logger.info(
                f"stop loss hit is {stop_loss.hit} and target hit is {target.hit}"
            )
            position_exists = positions.strike_exists(
                security_id=contract_security_id, position_type=position_type
            )
            if position_exists:
                logger.info(
                    f"stop loss hit is {stop_loss.hit} and target hit is {target.hit}"
                )
                return order.buy(security_id=contract_security_id, quantity=quantity)
            logger.info(
                f"returning to process_order as position_exists is {position_exists}"
            )
            return

import logging
import os
from datetime import datetime

import click
import debugpy
from contract import Contract
from minute_chart import MinuteChart
from option_type import OptionType
from order import LotSize, Order
from positions import Positions
from process_order import process_order
from strike_price import StrikePrice
from symbol_id import SymbolId
from utils import get_dhan_client, read_redis_queue
from weekly_expiry import WeeklyExpiry

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


if os.environ.get("DEBUG") == "True":
    debugpy.listen(("0.0.0.0", 5678))
    debugpy.wait_for_client()


@click.command()
@click.option("--symbol-name", required=True, help="name of symbol")
@click.option(
    "--exchange",
    type=click.Choice(["NSE", "BSE", "MCX"]),
    required=True,
    help="name of exchange",
)
@click.option(
    "--environment", type=click.Choice(["development", "production"]), required=True
)
@click.option("--download-directory", type=click.Path(), default="/download")
@click.option("--trade-symbols-file-name", default="api-scrip-master.csv")
@click.option(
    "--position-type",
    type=click.Choice(["SHORT", "LONG"]),
    default="SHORT",
    help="position type",
)
@click.option("--target-percent", default=80, help="target percent")
def main(
    download_directory: str,
    trade_symbols_file_name: str,
    symbol_name: str,
    exchange: str,
    environment: str,
    position_type: str,
    target_percent: int,
):
    dhan_client = get_dhan_client(environment=environment)
    symbols_file_path = f"{download_directory}/{symbol_name}-{trade_symbols_file_name}"
    while True:
        signal, candle_data = read_redis_queue()
        if not candle_data:
            continue
        signal = signal.decode("utf-8")
        logger.info(f"signal is {signal}")
        candle_data_timestamp = datetime.strptime(
            candle_data["timestamp"], "%Y-%m-%d %H:%M:%S"
        )
        current_time = datetime.now()
        logger.info(f"current time is {current_time}")
        if not (
            current_time.day == candle_data_timestamp.day
            and current_time.hour == candle_data_timestamp.hour
            and current_time.minute == candle_data_timestamp.minute
        ):
            logger.info(
                "SKIPPING as current timestamp and candle timestamp are not matching\n"
                f"current_time {current_time}\n"
                f"candlestick time {candle_data_timestamp}\n"
                f"candlestick data {candle_data}"
            )
            continue
        spot_price = candle_data.get("close")
        logger.info(f"spot_price is {spot_price}")
        strike_price = StrikePrice(
            symbol_name, spot_price, option_type=OptionType[signal].value
        )
        logger.info(
            f"current strike_price {strike_price.current}\n"
            f"required strike_price {strike_price.required}"
        )
        expiry = WeeklyExpiry(symbol_name)
        contract = Contract(
            symbol_name=symbol_name,
            strike_price=strike_price.required,
            type=signal,
            symbols_file_path=symbols_file_path,
            expiry=expiry,
        )
        positions = Positions(dhan_client=dhan_client)
        if positions.spot_exists(symbol_name=symbol_name, position_type=position_type):
            logger.info(
                f"position already exists for contract {contract.name} "
                f"and security_id {contract.security_id}"
            )
            continue
        order = Order(dhan_client=dhan_client)
        sell_order = order.sell(
            security_id=contract.security_id,
            quantity=LotSize[symbol_name].value,
        )
        logger.info(f"SELL order {sell_order.id} executed for {contract.name}")
        minute_chart = MinuteChart(dhan_client=dhan_client)
        process_order(
            minute_chart=minute_chart,
            order=order,
            symbol_security_id=SymbolId[symbol_name].value,
            contract_security_id=contract.security_id,
            ordered_candle=candle_data,
            quantity=LotSize[symbol_name].value,
            signal=signal,
            target_percent=target_percent,
            positions=positions,
            position_type=position_type,
            symbol_name=symbol_name,
        )


if __name__ == "__main__":
    main()

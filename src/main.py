import logging
import os
from datetime import datetime, timedelta

import click
import debugpy
import pandas as pd
from contract import Contract
from minute_chart import MinuteChart
from option_type import OptionType
from order import LotSize, Order
from positions import Positions
from process_order import process_order
from strike_price import StrikePrice
from symbol_id import SymbolId
from trading_hours import TradingHours
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
    trading_hours = TradingHours()
    positions = Positions(dhan_client=dhan_client)
    order = Order(dhan_client=dhan_client)
    if positions.spot_exists(symbol_name=symbol_name, position_type=position_type):
        logger.info("Open position exists even after reboot. closing it.")
        for position in positions.get:
            if position.get("positionType") == "SHORT":
                contract_security_id = position.get("securityId")
                quantity = position.get("sellQty")
                trading_symbol = position.get("tradingSymbol")
                logger.info(f"closing position for {trading_symbol}")
                order.buy(security_id=contract_security_id, quantity=quantity)
    contract_df = pd.read_csv(symbols_file_path)
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
        previous_candle_time = current_time - timedelta(minutes=5)
        logger.info(f"current time is {current_time}")
        logger.info(f"previous candle time is {previous_candle_time}")
        if not (
            previous_candle_time.day == candle_data_timestamp.day
            and previous_candle_time.hour == candle_data_timestamp.hour
            and previous_candle_time.minute == candle_data_timestamp.minute
        ):
            logger.info(
                "SKIPPING as previous candle timestamp is not matching\n"
                f"previous_candle_time {previous_candle_time}\n"
                f"candlestick time {candle_data_timestamp}\n"
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
            contract_df=contract_df,
            expiry=expiry,
        )
        if positions.spot_exists(symbol_name=symbol_name, position_type=position_type):
            logger.info(
                f"SKIPPING position already exists for contract {contract.name} "
                f"and security_id {contract.security_id}"
            )
            continue
        if not trading_hours.open_position:
            logger.info("SKIPPING non position open hour")
            continue
        sell_order = order.sell(
            security_id=contract.security_id,
            quantity=LotSize[symbol_name].value,
        )
        logger.info(f"RUNNING sell order {sell_order.id} executed for {contract.name}")
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
            trading_hours=trading_hours,
        )
        logger.info("next line after process_order function")


if __name__ == "__main__":
    main()

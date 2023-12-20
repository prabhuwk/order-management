import logging
import time

import click
from contract import Contract
from option_type import OptionType
from order import LotSize, Order
from strike_price import StrikePrice
from utils import get_dhan_client, read_redis_queue
from weekly_expiry import WeeklyExpiry

logging.basicConfig(
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


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
def main(
    download_directory: str,
    trade_symbols_file_name: str,
    symbol_name: str,
    exchange: str,
    environment: str,
):
    dhan_client = get_dhan_client(environment=environment)
    symbols_file_path = f"{download_directory}/{symbol_name}-{trade_symbols_file_name}"
    signals = ["BUY", "SELL"]
    while True:
        for signal in signals:
            data = read_redis_queue(signal)
            if data:
                spot_price = data.get("close")
                strike_price = StrikePrice(
                    symbol_name, spot_price, option_type=OptionType[signal].value
                )
                expiry = WeeklyExpiry(symbol_name)
                contract = Contract(
                    symbol_name=symbol_name,
                    strike_price=strike_price.required,
                    type=signal,
                    symbols_file_path=symbols_file_path,
                    expiry=expiry,
                )
                order = Order(dhan_client=dhan_client)
                if order.list:
                    continue
                sell_order = order.sell(
                    security_id=contract.id,
                    quantity=LotSize[symbol_name].value,
                )
                logger.info(sell_order.id)

        time.sleep(1)


if __name__ == "__main__":
    main()

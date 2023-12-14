import json
import time

import click
from utils import read_redis_queue


@click.command()
@click.option("--symbol-name", required=True, help="name of symbol")
@click.option(
    "--symbol-segment",
    type=click.Choice(["C", "D", "E", "I", "M"]),
    required=True,
    help="C=CURRENCY, D=DERIVATIVE, E=EQUITY, I=INDEX, M=COMMODITY",
)
@click.option(
    "--symbol-type",
    type=click.Choice(
        [
            "EQUITY",
            "FUTCOM",
            "FUTCUR",
            "FUTIDX",
            "FUTSTK",
            "INDEX",
            "OPTCUR",
            "OPTFUT",
            "OPTIDX",
            "OPTSTK",
        ]
    ),
    required=True,
    help="type of symbol",
)
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
@click.option("--candlestick-interval", default=5, help="candlestick interval")
@click.option("--trade-symbols-file-name", default="api-scrip-master.csv")
def main(
    download_directory: str,
    trade_symbols_file_name: str,
    symbol_name: str,
    symbol_segment: str,
    symbol_type: str,
    exchange: str,
    environment: str,
    candlestick_interval: int,
):
    while True:
        message = read_redis_queue("BUY")
        try:
            data = json.loads(message)
        except json.JSONDecodeError as e:
            print("error: ", e)
        print(data)
        time.sleep(1)


if __name__ == "__main__":
    main()

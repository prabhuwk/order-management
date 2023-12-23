import time

import click
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
    signals = ["BUY", "SELL"]
    while True:
        for signal in signals:
            data = read_redis_queue(signal)
            if not data:
                continue
            spot_price = data.get("close") if signal == "BUY" else data.get("open")
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
            positions = Positions(dhan_client=dhan_client)
            if positions.exists(
                security_id=contract.security_id, position_type=position_type
            ):
                continue
            order = Order(dhan_client=dhan_client)
            sell_order = order.sell(
                security_id=contract.security_id,
                quantity=LotSize[symbol_name].value,
            )
            click.secho(f"SELL order {sell_order.id} executed for {contract.name}")
            minute_chart = MinuteChart(dhan_client=dhan_client)
            process_order(
                minute_chart=minute_chart,
                order=order,
                symbol_id=SymbolId[symbol_name].value,
                security_id=contract.security_id,
                ordered_candle=data,
                quantity=LotSize[symbol_name].value,
                signal=signal,
                target_percent=target_percent,
            )
        time.sleep(0.5)


if __name__ == "__main__":
    main()

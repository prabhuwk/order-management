import re

import click
from contract import Contract
from minute_chart import MinuteChart
from option_type import OptionType
from order import LotSize, Order
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
                order = Order(dhan_client=dhan_client)
                order_list = order.list
                if order_list:
                    for single_order in order_list:
                        pattern = re.compile("(\w+)-\w+-\d+-\w+")
                        match = re.match(pattern, single_order.get("tradingSymbol"))
                        if match.groups()[0] == symbol_name:
                            click.secho(
                                f"{single_order.get('transactionType')} order already "
                                f"exists for {symbol_name}"
                            )
                            continue
                    continue
                sell_order = order.sell(
                    security_id=contract.id,
                    quantity=LotSize[symbol_name].value,
                )
                click.secho(f"SELL order {sell_order.id} executed for {contract.name}")
                minute_chart = MinuteChart(dhan_client=dhan_client)
                process_order(
                    minute_chart,
                    order,
                    symbol_id=SymbolId[symbol_name].value,
                    contract_id=contract.id,
                    ordered_candle=data,
                    quantity=LotSize[symbol_name].value,
                    signal=signal,
                )


if __name__ == "__main__":
    main()

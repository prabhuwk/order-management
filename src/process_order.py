from order import Order


def process_order(
    minute_chart, order: Order, symbol_id, contract_id, ordered_candle, quantity, signal
):
    current_candle = minute_chart.intraday(security_id=symbol_id)
    if signal == "BUY":
        if current_candle["low"][-1] < ordered_candle["low"]:
            order.buy(security_id=contract_id, quantity=quantity)

        elif current_candle["high"][-1] > ordered_candle["resistance"] - (
            (ordered_candle["resistance"] - ordered_candle["support"]) * 0.20
        ):
            order.buy(security_id=contract_id, quantity=quantity)

    if signal == "SELL":
        if current_candle["high"][-1] > ordered_candle["high"]:
            order.buy(security_id=contract_id, quantity=quantity)
        elif current_candle["low"][-1] > ordered_candle["support"] + (
            (ordered_candle["resistance"] - ordered_candle["support"]) * 0.20
        ):
            order.buy(security_id=contract_id, quantity=quantity)

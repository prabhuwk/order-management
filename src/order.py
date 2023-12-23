from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Literal

from dhanhq import dhanhq


class LotSize(Enum):
    MIDCPNIFTY = 75
    BANKNIFTY = 15
    NIFTY = 50
    FINNIFTY = 40
    SENSEX = 10


@dataclass(frozen=True)
class OrderInfo:
    id: str
    status: Literal["TRANSIT", "PENDING", "REJECTED", "CANCELLED", "TRADED", "EXPIRED"]


class Order:
    def __init__(self, dhan_client: dhanhq):
        self.dhan_client = dhan_client

    @property
    def list(self) -> List:
        order_list = self.dhan_client.get_order_list()
        if order_list.get("status") == "success":
            return order_list.get("data")
        return None

    def get(self, order_id: int) -> Dict:
        get_order = self.dhan_client.get_order_by_id(order_id=order_id)
        if get_order.get("status") == "success":
            return get_order.get("data")
        return None

    def sell(self, security_id: str, quantity: int) -> OrderInfo:
        sell_order = self.dhan_client.place_order(
            security_id=security_id,
            exchange_segment=self.dhan_client.FNO,
            transaction_type=self.dhan_client.SELL,
            quantity=quantity,
            order_type=self.dhan_client.MARKET,
            product_type=self.dhan_client.INTRA,
            price=0,
        )
        if sell_order.get("status") == "success":
            return OrderInfo(
                id=sell_order.get("data").get("orderId"),
                status=sell_order.get("data").get("orderStatus"),
            )

    def buy(self, security_id: str, quantity: int) -> OrderInfo:
        buy_order = self.dhan_client.place_order(
            security_id=security_id,
            exchange_segment=self.dhan_client.FNO,
            transaction_type=self.dhan_client.BUY,
            quantity=quantity,
            order_type=self.dhan_client.MARKET,
            product_type=self.dhan_client.INTRA,
            price=0,
        )
        if buy_order.get("status") == "success":
            return OrderInfo(
                id=buy_order.get("data").get("orderId"),
                status=buy_order.get("data").get("orderStatus"),
            )

    def limit(self, security_id: str, quantity: int) -> OrderInfo:
        limit_order = self.dhan_client.place_order(
            security_id=security_id,
            exchange_segment=self.dhan_client.FNO,
            transaction_type=self.dhan_client.LIMIT,
            quantity=quantity,
            order_type=self.dhan_client.MARKET,
            product_type=self.dhan_client.INTRA,
            price=0,
        )
        if limit_order.get("status") == "success":
            return OrderInfo(
                id=limit_order.get("data").get("orderId"),
                status=limit_order.get("data").get("orderStatus"),
            )

    def stop_limit(self, security_id: str, quantity: int) -> OrderInfo:
        stop_limit_order = self.dhan_client.place_order(
            security_id=security_id,
            exchange_segment=self.dhan_client.FNO,
            transaction_type=self.dhan_client.STOP_LIMIT,
            quantity=quantity,
            order_type=self.dhan_client.MARKET,
            product_type=self.dhan_client.INTRA,
            price=0,
        )
        if stop_limit_order.get("status") == "success":
            return OrderInfo(
                id=stop_limit_order.get("data").get("orderId"),
                status=stop_limit_order.get("data").get("orderStatus"),
            )

    def modify(
        self,
        order_id: str,
        order_type,
        leg_name: str,
        quantity: int,
        price: float,
        trigger_price: float,
        disclosed_quantity: int,
        validity: str,
    ):
        return self.dhan_client.modify_order(
            order_id,
            order_type,
            leg_name,
            quantity,
            price,
            trigger_price,
            disclosed_quantity,
            validity,
        )

    def cancel(self, order_id: int):
        return self.dhan_client.cancel_order(order_id=order_id)

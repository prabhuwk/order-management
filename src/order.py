from enum import Enum


class LotSize(Enum):
    MIDCPNIFTY = 75
    BANKNIFTY = 15
    NIFTY = 50
    FINNIFTY = 40
    SENSEX = 10


class Order:
    def __init__(self, dhan_client):
        self.dhan_client = dhan_client

    def list(self):
        order_list = self.dhan_client.get_order_list()
        if order_list.get("status") == "success":
            return order_list.data
        return None

    def get(self, order_id: int):
        return self.dhan_client.get_order_by_id(order_id=order_id)

    def place(self, security_id: str, transaction_type: str, quantity: int):
        return self.dhan_client.place_order(
            security_id=security_id,
            exchange_segment=self.dhan_client.FNO,
            transaction_type=self.dhan_client[transaction_type],
            quantity=quantity,
            order_type=self.dhan_client.MARKET,
            product_type=self.dhan_client.INTRA,
            price=0,
        )

    def modify(
        self,
        order_id,
        order_type,
        leg_name,
        quantity,
        price,
        trigger_price,
        disclosed_quantity,
        validity,
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

    def exists(self, security_id: str, transaction_type: str) -> bool:
        orders = self.list()
        for order in orders:
            if (
                order.get("securityId") == security_id
                and order.get("transactionType") == transaction_type
            ):
                return True
        return False

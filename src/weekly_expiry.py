from datetime import date as datetime_date
from datetime import timedelta
from enum import Enum
from functools import cached_property


class ExpiryDays(Enum):
    MIDCPNIFTY = 0
    FINNIFTY = 1
    BANKNIFTY = 2
    NIFTY = 3
    SENSEX = 4


class WeeklyExpiry:
    def __init__(self, symbol_name: str):
        self.symbol_name = symbol_name
        self.day_ = ExpiryDays[self.symbol_name].value

    @cached_property
    def date_(self) -> datetime_date:
        current_date = datetime_date.today()
        days_to_add = (self.day_ - current_date.weekday() + 7) % 7
        if days_to_add == 0:
            days_to_add = 7
        return current_date + timedelta(days=days_to_add)

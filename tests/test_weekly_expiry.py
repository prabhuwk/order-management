import datetime

from src.weekly_expiry import WeeklyExpiry


class TestWeeklyExpiry:
    def test_init(self, symbol_name="NIFTY"):
        weekly_expiry = WeeklyExpiry(symbol_name)
        assert weekly_expiry.symbol_name == symbol_name
        assert weekly_expiry.day_ == 3

    def test_date_(self, symbol_name="NIFTY"):
        weekly_expiry = WeeklyExpiry(symbol_name)
        current_date = datetime.date.today()
        days_to_add = (weekly_expiry.day_ - current_date.weekday() + 7) % 7
        if days_to_add == 0:
            days_to_add = 7
        weekly_expiry_date = current_date + datetime.timedelta(days=days_to_add)
        assert weekly_expiry.date_ == weekly_expiry_date

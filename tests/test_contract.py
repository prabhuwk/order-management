from datetime import date as datetime_date

from src.contract import Contract
from src.weekly_expiry import WeeklyExpiry


class TestContract:
    def test_init(self, mock_symbol_file):
        mock_weekly_expiry = WeeklyExpiry("NIFTY")
        mock_weekly_expiry.date_ = datetime_date(2024, 1, 25)
        mock_contract = Contract(
            symbol_name="NIFTY",
            strike_price=21900,
            type="BUY",
            symbols_file_path=mock_symbol_file,
            expiry=mock_weekly_expiry,
        )
        assert mock_contract.name == "NIFTY 25 JAN 21900 PUT"
        assert mock_contract.security_id == "35055"

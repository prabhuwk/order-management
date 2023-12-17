import pandas as pd
from weekly_expiry import WeeklyExpiry


class Contracts:
    def __init__(
        self,
        symbol_name: str,
        strike_price: int,
        type: str,
        symbols_file_path: str,
    ) -> None:
        self.type = type
        self.strike_price = strike_price
        self.symbol_name = symbol_name
        self.symbols_file_path = symbols_file_path
        self.expiry = WeeklyExpiry(self.symbol_name)

    @property
    def name(self) -> str:
        expiry_day = self.expiry.date_.day
        expiry_month = self.expiry.date_.strftime("%b").upper()
        return (
            f"{self.symbol_name} {expiry_day} "
            f"{expiry_month} {self.strike_price} {self.type}"
        )

    def get(self):
        df = pd.DataFrame(self.symbols_file_path)
        if self.name in df["SEM_CUSTOM_SYMBOL"].values:
            return df[df["SEM_CUSTOM_SYMBOL"] == self.name]
        df["SEM_EXPIRY_DATE"] = pd.to_datetime(df["SEM_EXPIRY_DATE"])
        nearest_date = min(
            df["SEM_EXPIRY_DATE"], key=lambda x: abs(x - self.expiry.date_)
        )
        return df[df["SEM_EXPIRY_DATE"] == nearest_date]

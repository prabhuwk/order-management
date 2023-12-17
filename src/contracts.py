import re
from datetime import datetime
from functools import cached_property

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
        self.expiry_day = self.expiry.date_.day
        self.expiry_month = self.expiry.date_.strftime("%b").upper()

    @cached_property
    def name(self) -> str:
        return (
            f"{self.symbol_name} {self.expiry_day} "
            f"{self.expiry_month} {self.strike_price} {self.type}"
        )

    @property
    def details(self):
        df = pd.read_csv(self.symbols_file_path)
        if self.name in df["SEM_CUSTOM_SYMBOL"].values:
            return df[df["SEM_CUSTOM_SYMBOL"] == self.name]
        pattern = re.compile(
            f"{self.symbol_name} ([0-9]+) {self.expiry_month} "
            f"{self.strike_price} {self.type}"
        )
        matched_rows = df[df["SEM_CUSTOM_SYMBOL"].str.match(pattern)]
        today = pd.Timestamp(datetime.now().strftime("%Y-%m-%d"))
        matched_rows["SEM_EXPIRY_DATE"] = pd.to_datetime(
            matched_rows["SEM_EXPIRY_DATE"]
        )

        future_dates = matched_rows[matched_rows["SEM_EXPIRY_DATE"] > today]
        next_date = future_dates["SEM_EXPIRY_DATE"].min()
        return future_dates[future_dates["SEM_EXPIRY_DATE"] == next_date]

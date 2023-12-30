import re
from datetime import datetime

import pandas as pd
from option_type import OptionType


class Contract:
    def __init__(
        self,
        symbol_name: str,
        strike_price: int,
        type: str,
        contract_df: str,
        expiry: int,
    ) -> None:
        self.type = OptionType[type].value
        self.strike_price = strike_price
        self.symbol_name = symbol_name
        self.contract_df = contract_df
        self.expiry_day = expiry.date_.day
        self.expiry_month = expiry.date_.strftime("%b").upper()
        self.name = self._name()
        self.security_id = self._security_id()

    def _name(self) -> str:
        return (
            f"{self.symbol_name} {self.expiry_day} "
            f"{self.expiry_month} {self.strike_price} {self.type}"
        )

    def _security_id(self) -> str:
        if self.name in self.contract_df["SEM_CUSTOM_SYMBOL"].values:
            match = self.contract_df[self.contract_df["SEM_CUSTOM_SYMBOL"] == self.name]
            return str(match["SEM_SMST_SECURITY_ID"].values[0])
        pattern = re.compile(
            f"{self.symbol_name} ([0-9]+) {self.expiry_month} "
            f"{self.strike_price} {self.type}"
        )
        matched_rows = self.contract_df[
            self.contract_df["SEM_CUSTOM_SYMBOL"].str.match(pattern)
        ]
        today = pd.Timestamp(datetime.now().strftime("%Y-%m-%d"))
        matched_rows.loc[:, "SEM_EXPIRY_DATE"] = pd.to_datetime(
            matched_rows["SEM_EXPIRY_DATE"]
        )
        future_dates = matched_rows[matched_rows["SEM_EXPIRY_DATE"] > today]
        next_date = future_dates["SEM_EXPIRY_DATE"].min()
        match = future_dates[future_dates["SEM_EXPIRY_DATE"] == next_date]
        return str(match["SEM_SMST_SECURITY_ID"].values[0])

from typing import Dict

from dhanhq import dhanhq


class MinuteChart:
    def __init__(self, dhan_client: dhanhq) -> None:
        self._dhan_client = dhan_client
        self._instrument_type = "INDEX"
        self._exchange_segment = "IDX_I"

    def intraday(self, security_id: str) -> Dict:
        minute_chart = self._dhan_client.intraday_daily_minute_charts(
            security_id=security_id,
            exchange_segment=self._exchange_segment,
            instrument_type=self._instrument_type,
        )
        return minute_chart["data"]

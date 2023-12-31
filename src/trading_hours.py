from dataclasses import dataclass, field
from datetime import datetime, time
from enum import Enum


class OpenPosition(Enum):
    START_TIME = time(9, 15)
    END_TIME = time(15, 0)


class ClosePosition(Enum):
    START_TIME = time(9, 15)
    END_TIME = time(15, 29)


@dataclass
class TradingHours:
    open_position: bool = field(init=False)
    close_position: bool = field(init=False)

    def __post_init__(self):
        self._time = datetime.now()
        self.open_position = self._open_position()
        self.close_position = self._close_position()

    def _weekday(self):
        return self._time.weekday() >= 5

    def _open_position(self):
        return (
            self._weekday()
            and OpenPosition.START_TIME.value
            <= self._time.time()
            <= OpenPosition.END_TIME.value
        )

    def _close_position(self):
        return (
            self._weekday()
            and ClosePosition.START_TIME.value
            <= self._time.time()
            <= ClosePosition.END_TIME.value
        )

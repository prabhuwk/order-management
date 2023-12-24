import json
from pathlib import Path

import pytest
from dhanhq import dhanhq


@pytest.fixture
def fixture_path():
    return f"{Path(__file__).parent}/fixtures"


@pytest.fixture
def minute_chart_file(fixture_path):
    return f"{fixture_path}/minute_chart.json"


@pytest.fixture
def mock_minute_chart(minute_chart_file):
    with open(minute_chart_file) as f:
        return json.load(f)


@pytest.fixture
def sell_candle_file(fixture_path):
    return f"{fixture_path}/sell_candle.json"


@pytest.fixture
def sell_candle(sell_candle_file):
    with open(sell_candle_file) as f:
        return json.load(f)


@pytest.fixture
def mock_dhan_client(mocker) -> dhanhq:
    return mocker.Mock(spec=dhanhq)


@pytest.fixture
def mock_positions_output() -> dict:
    return {
        "data": [
            {
                "positionType": "SHORT",
                "securityId": "52428",
            }
        ],
        "remarks": "",
        "status": "success",
    }


@pytest.fixture
def mock_symbol_file(fixture_path):
    return f"{fixture_path}/symbols.csv"

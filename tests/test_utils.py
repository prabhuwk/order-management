import os

from dhanhq import dhanhq

from src.utils import get_dhan_client


def test_get_dhan_client(mocker) -> dhanhq:
    mocker.patch.dict(
        os.environ,
        {"DHAN_CLIENT_ID": "123456", "DHAN_ACCESS_TOKEN": "mock-access-token"},
    )
    dhan_client = get_dhan_client(environment="development")
    assert type(dhan_client) == dhanhq

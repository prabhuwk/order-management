import json
import logging
import os
from functools import lru_cache

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dhanhq import dhanhq
from dotenv import load_dotenv
from redis import Redis


class ClientIdAccessTokenNotFoundError(Exception):
    """Client ID and Access Token not found"""


def get_keyvault_secret_client() -> SecretClient:
    keyvault_url = os.environ.get("KEYVAULT_URL")
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=keyvault_url, credential=credential)


def get_dhan_client(environment: str) -> dhanhq:
    if environment == "development":
        load_dotenv()
        if "DHAN_CLIENT_ID" not in os.environ and "DHAN_ACCESS_TOKEN" not in os.environ:
            raise ClientIdAccessTokenNotFoundError(
                "Please set DHAN_CLIENT_ID and DHAN_ACCESS_TOKEN for authentication."
            )
        client_id = os.environ.get("DHAN_CLIENT_ID")
        access_token = os.environ.get("DHAN_ACCESS_TOKEN")
        return dhanhq(client_id, access_token)
    secret_client = get_keyvault_secret_client()
    client_id = secret_client.get_secret("DHAN-CLIENT-ID").value
    access_token = secret_client.get_secret("DHAN-ACCESS-TOKEN").value
    return dhanhq(client_id, access_token)


@lru_cache
def get_redis_client() -> Redis:
    host = os.environ.get("REDIS_HOST")
    port = os.environ.get("REDIS_PORT")
    db = 0
    return Redis(host=host, port=port, db=db)


def read_redis_queue(queue_name: str) -> dict:
    redis_client = get_redis_client()
    message = redis_client.blpop(queue_name, 1)
    if message:
        data = message[1].decode("utf-8")
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid json data from redis queue. {e}")
    return None

import json
import logging
import os
from functools import lru_cache

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dhanhq import dhanhq
from dotenv import load_dotenv
from redis import Redis

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


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


def read_redis_queue() -> dict:
    redis_client = get_redis_client()
    item = redis_client.blpop(["BUY", "SELL"], 15)
    if not item:
        return None, None
    queue_name, message = item
    if message:
        try:
            logger.info(f"found data in redis queue {queue_name}")
            return queue_name, json.loads(message)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid json data from redis queue. {e}")
    return None, None

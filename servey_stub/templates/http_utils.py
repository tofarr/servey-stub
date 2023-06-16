import requests
from marshy.types import ExternalItemType, ExternalType


def invoke(
    url: str, method: str, event: ExternalItemType, timeout: int = 15
) -> ExternalType:
    if method.upper() in ("POST", "PUT", "PATCH"):
        response = requests.request(method, url, json=event, timeout=timeout)
    else:
        response = requests.request(method, url, params=event, timeout=timeout)
    return response.json()

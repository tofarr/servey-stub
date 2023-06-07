import requests
from marshy.types import ExternalItemType, ExternalType


def invoke(url: str, method: str, event: ExternalItemType) -> ExternalType:
    if method.upper() in ("POST", "PUT", "PATCH"):
        response = requests.request(method, url, json=event)
    else:
        response = requests.request(method, url, params=event)
    return response.json()

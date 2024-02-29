from typing import Optional
import requests
from marshy.types import ExternalItemType, ExternalType


def invoke(
    url: str,
    method: str,
    event: ExternalItemType,
    authorization: Optional[str] = None,
    timeout: int = 15,
) -> ExternalType:
    headers = {}
    if authorization:
        headers["Authorization"] = "Bearer " + authorization
    if method.upper() in ("POST", "PUT", "PATCH"):
        response = requests.request(
            method, url, json=event, headers=headers, timeout=timeout
        )
    else:
        response = requests.request(
            method, url, params=event, headers=headers, timeout=timeout
        )
    return response.json()

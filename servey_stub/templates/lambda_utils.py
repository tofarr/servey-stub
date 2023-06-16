import json
import typing
import boto3
from marshy.types import ExternalType

_lambda_client = None


def get_lambda_client():
    # pylint: disable=W0603
    global _lambda_client
    if not _lambda_client:
        _lambda_client = boto3.client("lambda")
    return _lambda_client


def invoke(
    function_name: str, event: typing.Dict, invocation_type: str = "RequestResponse"
) -> ExternalType:
    request_payload = json.dumps(event)
    response = get_lambda_client().invoke(
        FunctionName=function_name,
        InvocationType=invocation_type,
        Payload=request_payload,
    )
    response_payload = response.get("Payload")
    if response_payload:
        data = json.load(response_payload)
        return data

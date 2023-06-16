from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

import servey_stub
from servey_stub.lambda_service_definition import LambdaServiceDefinition
from tests.fixtures import ACTIONS, create_mock_file_system


class TestLambdaServiceDefinition(TestCase):
    def test_generate_service_code(self):
        service = LambdaServiceDefinition(actions=ACTIONS, service_name="greeter")
        mock_file_system = create_mock_file_system(
            Path(Path(servey_stub.__file__).parent, "templates", "setup.txt"),
            Path(Path(servey_stub.__file__).parent, "templates", "lambda_utils.py"),
        )
        with (
            patch("os.path.exists", mock_file_system.exists),
            patch("builtins.open", mock_file_system.open),
            patch("pathlib.PosixPath.mkdir", mock_file_system.mkdir),
        ):
            service.generate_service_code()
        contents = {
            str(k): [s for s in v.getvalue().split("\n") if not s.startswith("#")]
            for k, v in mock_file_system.contents.items()
            if "/templates/" not in str(k)
        }
        expected_contents = {
            "servey_stub/greeter_lambda/greeter/__init__.py": [""],
            "servey_stub/greeter_lambda/greeter/models/__init__.py": [""],
            "servey_stub/greeter_lambda/greeter/lambda_utils.py": [
                "import json",
                "import typing",
                "import boto3",
                "from marshy.types import ExternalType",
                "",
                "_lambda_client = None",
                "",
                "",
                "def get_lambda_client():",
                "    # pylint: disable=W0603",
                "    global _lambda_client",
                "    if not _lambda_client:",
                '        _lambda_client = boto3.client("lambda")',
                "    return _lambda_client",
                "",
                "",
                "def invoke(",
                '    function_name: str, event: typing.Dict, invocation_type: str = "RequestResponse"',
                ") -> ExternalType:",
                "    request_payload = json.dumps(event)",
                "    response = get_lambda_client().invoke(",
                "        FunctionName=function_name,",
                "        InvocationType=invocation_type,",
                "        Payload=request_payload,",
                "    )",
                '    response_payload = response.get("Payload")',
                "    if response_payload:",
                "        data = json.load(response_payload)",
                "        return data",
                "",
            ],
            "servey_stub/greeter_lambda/greeter/models/number_stats.py": [
                "from dataclasses import dataclass",
                "",
                "",
                "@dataclass",
                "class NumberStats:",
                "    name: str",
                "    value: int",
                "",
            ],
            "servey_stub/greeter_lambda/greeter/greeter.py": [
                "from greeter import lambda_utils",
                "from greeter.models.number_stats import NumberStats",
                "import marshy",
                "",
                "",
                "class Greeter:",
                "",
                '    def say_hello(self, name: str = "User"):',
                "        event_ = {",
                '            "action_name": "say_hello",',
                '            "params": {',
                '                "name": marshy.dump(name, str),',
                "            }",
                "        }",
                '        result_ = lambda_utils.invoke_lambda("ServeyMain-dev-say_hello", event_)',
                "        loaded_result_ = marshy.load(str, result_)",
                "        return loaded_result_",
                "",
                "",
                "    def save_number_stats(self, number_stats: NumberStats, insert: bool = False):",
                "        event_ = {",
                '            "action_name": "save_number_stats",',
                '            "params": {',
                '                "number_stats": marshy.dump(number_stats, NumberStats),',
                '                "insert": marshy.dump(insert, bool),',
                "            }",
                "        }",
                '        result_ = lambda_utils.invoke_lambda("ServeyMain-dev-save_number_stats", event_)',
                "        loaded_result_ = marshy.load(int, result_)",
                "        return loaded_result_",
                "",
                "",
                "",
            ],
            "servey_stub/greeter_lambda/setup.py": [
                "import setuptools",
                "",
                "setuptools.setup(",
                '    name="greeter",',
                '    version="0.1.0",',
                '    packages=setuptools.find_packages(exclude=("tests*")),',
                "    install_requires=['boto3', 'marshy'],",
                ")",
                "",
            ],
        }
        self.assertEqual(expected_contents, contents)

from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

import servey_stub
from servey_stub.http_service_definition import HttpServiceDefinition
from tests.fixtures import ACTIONS, create_mock_file_system


class TestHttpServiceDefinition(TestCase):
    def test_generate_service_code(self):
        service = HttpServiceDefinition(
            actions=ACTIONS,
            service_name="greeter",
            service_root_url="https://greeter.com",
        )
        mock_file_system = create_mock_file_system(
            Path(Path(servey_stub.__file__).parent, "templates", "setup.txt"),
            Path(Path(servey_stub.__file__).parent, "templates", "http_utils.py"),
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
            "servey_stub/greeter_http/greeter/__init__.py": [""],
            "servey_stub/greeter_http/greeter/models/__init__.py": [""],
            "servey_stub/greeter_http/greeter/http_utils.py": [
                "import requests",
                "from marshy.types import ExternalItemType, ExternalType",
                "",
                "",
                "def invoke(",
                "    url: str, method: str, event: ExternalItemType, timeout: int = 15",
                ") -> ExternalType:",
                '    if method.upper() in ("POST", "PUT", "PATCH"):',
                "        response = requests.request(method, url, json=event, timeout=timeout)",
                "    else:",
                "        response = requests.request(method, url, params=event, timeout=timeout)",
                "    return response.json()",
                "",
            ],
            "servey_stub/greeter_http/greeter/models/number_stats.py": [
                "from dataclasses import dataclass",
                "",
                "",
                "@dataclass",
                "class NumberStats:",
                "    name: str",
                "    value: int",
                "",
            ],
            "servey_stub/greeter_http/greeter/greeter.py": [
                "from greeter import http_utils",
                "from greeter.models.number_stats import NumberStats",
                "import marshy",
                "",
                "",
                "class Greeter:",
                "",
                '    def say_hello(self, name: str = "User"):',
                "        event_ = {",
                '            "name": marshy.dump(name, str),',
                "        }",
                '        result_ = http_utils.invoke("https://greeter.com/say-hello", "get", event_, 15)',
                "        loaded_result_ = marshy.load(result_)",
                "        return loaded_result_",
                "",
                "",
                "    def save_number_stats(self, number_stats: NumberStats, insert: bool = False):",
                "        event_ = {",
                '            "number_stats": marshy.dump(number_stats, NumberStats),',
                '            "insert": marshy.dump(insert, bool),',
                "        }",
                '        result_ = http_utils.invoke("https://greeter.com/save-number-stats", "post", event_, 15)',
                "        loaded_result_ = marshy.load(result_)",
                "        return loaded_result_",
                "",
                "",
                "",
            ],
            "servey_stub/greeter_http/setup.py": [
                "import setuptools",
                "",
                "setuptools.setup(",
                '    name="greeter",',
                '    version="0.1.0",',
                '    packages=setuptools.find_packages(exclude=("tests*")),',
                "    install_requires=['marshy', 'requests'],",
                ")",
                "",
            ],
        }
        self.assertEqual(expected_contents, contents)

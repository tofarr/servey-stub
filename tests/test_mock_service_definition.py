from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

import servey_stub
from servey_stub.mock_service_definition import MockServiceDefinition
from tests.fixtures import ACTIONS, create_mock_file_system


class TestMockServiceDefinition(TestCase):
    def test_generate_service_code(self):
        service = MockServiceDefinition(actions=ACTIONS, service_name="greeter")
        mock_file_system = create_mock_file_system(
            Path(Path(servey_stub.__file__).parent, "templates", "setup.txt"),
            Path(Path(servey_stub.__file__).parent, "templates", "mock_utils.py"),
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
            "servey_stub/greeter_mock/greeter/__init__.py": [""],
            "servey_stub/greeter_mock/greeter/models/__init__.py": [""],
            "servey_stub/greeter_mock/greeter/mock_utils.py": [
                "from typing import List, Tuple, Dict, Optional, Callable",
                "",
                "from marshy.types import ExternalItemType, ExternalType",
                "",
                "from servey_stub.errors import StubError",
                "",
                "",
                "def get_mock_result(",
                "    action_name: str,",
                "    event: ExternalItemType,",
                "    mocks: Dict[str, List[Tuple[ExternalItemType, ExternalType]]],",
                "):",
                "    custom_handler = get_custom_handler(action_name)",
                "    if custom_handler:",
                "        result = custom_handler(event)",
                "        return result",
                "    action_mocks = mocks.get(action_name) or []",
                "    for params, result in action_mocks:",
                "        if event == params:",
                "            return result",
                '    raise StubError("no_mock_for_event")',
                "",
                "",
                "def get_custom_handler(",
                "    action_name: str,",
                ") -> Optional[Callable[[ExternalItemType], ExternalType]]:",
                "    try:",
                "        # noinspection PyUnresolvedReferences",
                "        from . import custom_mocks",
                "",
                "        return getattr(custom_mocks, action_name)",
                "    except ModuleNotFoundError:",
                "        return None",
                "",
            ],
            "servey_stub/greeter_mock/greeter/models/number_stats.py": [
                "from dataclasses import dataclass",
                "",
                "",
                "@dataclass",
                "class NumberStats:",
                "    name: str",
                "    value: int",
                "",
            ],
            "servey_stub/greeter_mock/greeter/greeter.py": [
                "from greeter import mock_utils",
                "from greeter.models.number_stats import NumberStats",
                "import marshy",
                "",
                "",
                'MOCKS = {"say_hello": [[{"name": "Dev"}, "Hello Dev!"]], "save_number_stats": [[{"number_stats": {"name": "one", "value": 1}}, 1]]}',
                "",
                "",
                "class Greeter:",
                "",
                '    def say_hello(self, name: str = "User"):',
                "        event_ = {",
                '            "name": marshy.dump(name, str),',
                "        }",
                '        result_ = mock_utils.get_mock_result("say_hello", event_, MOCKS)',
                "        loaded_result_ = marshy.load(result_)",
                "        return loaded_result_",
                "",
                "",
                "    def save_number_stats(self, number_stats: NumberStats, insert: bool = False):",
                "        event_ = {",
                '            "number_stats": marshy.dump(number_stats, NumberStats),',
                '            "insert": marshy.dump(insert, bool),',
                "        }",
                '        result_ = mock_utils.get_mock_result("save_number_stats", event_, MOCKS)',
                "        loaded_result_ = marshy.load(result_)",
                "        return loaded_result_",
                "",
                "",
                "",
            ],
            "servey_stub/greeter_mock/setup.py": [
                "import setuptools",
                "",
                "setuptools.setup(",
                '    name="greeter",',
                '    version="0.1.0",',
                '    packages=setuptools.find_packages(exclude=("tests*")),',
                "    install_requires=['marshy'],",
                ")",
                "",
            ],
        }
        self.assertEqual(expected_contents, contents)

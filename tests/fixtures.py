from dataclasses import dataclass

from servey.action.action import get_action, action
from servey.action.example import Example
from servey.trigger.web_trigger import WEB_GET, WEB_POST

from tests.mock_file_system import ResetOnCloseStringIO, MockFileSystem


@dataclass
class NumberStats:
    name: str
    value: int


@action(
    triggers=WEB_GET,
    examples=(Example(name="dev", params={"name": "Dev"}, result="Hello Dev!"),),
)
def say_hello(name: str = "User") -> str:
    """Just a dummy"""


@action(
    triggers=WEB_POST,
    examples=(
        Example(
            name="one", params={"number_stats": {"name": "one", "value": 1}}, result=1
        ),
    ),
)
def save_number_stats(number_stats: NumberStats, insert: bool = False) -> int:
    """Just a dummy"""


ACTIONS = [get_action(say_hello), get_action(save_number_stats)]


def create_mock_file_system(*args) -> MockFileSystem:
    contents = {}
    for path in args:
        with open(path, "r") as reader:
            path_contents = reader.read()
            contents[path] = ResetOnCloseStringIO(path_contents)
    mock_file_system = MockFileSystem(contents)
    return mock_file_system

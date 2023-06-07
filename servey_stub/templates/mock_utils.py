from typing import List, Tuple, Dict, Optional, Callable

from marshy.types import ExternalItemType, ExternalType

from servey_stub.errors import StubError


def get_mock_result(
    action_name: str,
    event: ExternalItemType,
    mocks: Dict[str, List[Tuple[ExternalItemType, ExternalType]]],
):
    custom_handler = get_custom_handler(action_name)
    if custom_handler:
        result = custom_handler(event)
        return result
    action_mocks = mocks.get(action_name) or []
    for params, result in action_mocks:
        if event == params:
            return result
    raise StubError("no_mock_for_event")


def get_custom_handler(
    action_name: str,
) -> Optional[Callable[[ExternalItemType], ExternalType]]:
    try:
        # noinspection PyUnresolvedReferences
        from . import custom_mocks

        return getattr(custom_mocks, action_name)
    except ModuleNotFoundError:
        return None

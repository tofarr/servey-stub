import argparse
from pathlib import Path

from servey.finder.action_finder_abc import find_actions_with_trigger_type
from servey.trigger.web_trigger import WebTrigger


def main():
    parser = argparse.ArgumentParser(description="Servey")
    parser.add_argument("--mode", required=True)
    parser.add_argument("--dir", default="servey_stub")
    parser.add_argument("--only", default="")
    parser.add_argument("--exclude", default="")
    args, _ = parser.parse_known_args()
    mode = args.mode
    if mode == "lambdas":
        from servey_stub.lambda_service_definition import (
            LambdaServiceDefinition as Service,
        )
    elif mode == "http":
        from servey_stub.http_service_definition import HttpServiceDefinition as Service
    elif mode == "mock":
        from servey_stub.mock_service_definition import MockServiceDefinition as Service
    else:
        raise ValueError(f"invalid_mode:{args.mode}")
    actions = [action for action, trigger in find_actions_with_trigger_type(WebTrigger)]
    if args.only:
        only = [e.strip() for e in args.only.split(",")]
        actions = [action for action in actions if action.name in only]
    elif args.exclude:
        exclude = [e.strip() for e in args.exclude.split(",")]
        actions = [action for action in actions if action.name not in exclude]
    service = Service(actions=actions, output_dir=Path(args.dir))
    service.generate_service_code()


if __name__ == "__main__":
    main()

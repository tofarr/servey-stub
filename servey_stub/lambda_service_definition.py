import inspect
import os
from dataclasses import dataclass, field
from io import IOBase
from pathlib import Path
from typing import List, Tuple

from servey.action.action import Action
from servey.util import get_servey_main

import servey_stub
from servey_stub.service_definition_abc import ServiceDefinitionABC
from servey_stub.type_definition.imports_definition import ImportsDefinition
from servey_stub.type_definition.type_definition_context import TypeDefinitionContext
from servey_stub.utils import get_existing_content, update_file


def _default_lambda_name_pattern() -> str:
    servey_main = get_servey_main().title().replace("_", "")
    return servey_main + "-dev-{fn_name}"


@dataclass
class LambdaServiceDefinition(ServiceDefinitionABC):
    lambda_name_pattern: str = field(default_factory=_default_lambda_name_pattern)
    use_router_for_all: bool = field(
        default_factory=lambda: int(os.environ.get("SERVEY_AWS_ROUTER_FOR_ALL", "0"))
        == 1
    )
    router_name: str = "servey_router"
    install_requires: List[str] = field(default_factory=lambda: ["boto3", "marshy"])

    def generate_scaffold_pys(self, package_dir: Path, models_dir: Path):
        super().generate_scaffold_pys(package_dir, models_dir)
        update_file(
            Path(package_dir, "lambda_utils.py"),
            get_existing_content(
                Path(Path(servey_stub.__file__).parent, "templates", "lambda_utils.py")
            ),
        )

    def create_models(
        self, model_dir: Path, model_package_name: str
    ) -> Tuple[ImportsDefinition, TypeDefinitionContext]:
        imports, type_definition_context = super().create_models(
            model_dir, model_package_name
        )
        imports.add(["marshy"])
        imports.add([self.service_name, "lambda_utils"])
        imports = imports.optimize()
        return imports, type_definition_context

    def write_function_body(
        self,
        action: Action,
        sig: inspect.Signature,
        context: TypeDefinitionContext,
        writer: IOBase,
    ):
        writer.write('        event_ = {\n            "action_name": "')
        writer.write(action.name)
        writer.write('",\n            "params": {\n')
        for param in sig.parameters.values():
            writer.write('                "')
            writer.write(param.name)
            writer.write('": marshy.dump(')
            writer.write(param.name)
            writer.write(", ")
            type_name = getattr(param.annotation, "__name__", None) or str(
                param.annotation
            )
            writer.write(type_name)
            writer.write("),\n")
        writer.write("            }\n        }\n")
        writer.write('        result_ = lambda_utils.invoke_lambda("')
        use_router = self.use_router_for_all or "<locals>" in action.fn.__qualname__
        fn_name = self.router_name if use_router else action.name
        writer.write(self.lambda_name_pattern.format(fn_name=fn_name))
        writer.write('", event_)\n')
        result_type_name = getattr(sig.return_annotation, "__name__", None) or str(
            sig.return_annotation
        )
        writer.write("        loaded_result_ = marshy.load(")
        writer.write(result_type_name)
        writer.write(", result_)\n        return loaded_result_\n\n")

import inspect
import os
from dataclasses import dataclass, field
from io import IOBase
from pathlib import Path
from typing import List, Tuple

from servey.action.action import Action
from servey.trigger.web_trigger import WebTrigger

import servey_stub
from servey_stub.service_definition_abc import ServiceDefinitionABC
from servey_stub.type_definition.imports_definition import ImportsDefinition
from servey_stub.type_definition.type_definition_context import TypeDefinitionContext
from servey_stub.utils import update_file, get_existing_content


@dataclass
class HttpServiceDefinition(ServiceDefinitionABC):
    install_requires: List[str] = field(default_factory=lambda: ["marshy", "requests"])
    service_root_url: str = field(default_factory=lambda: os.environ.get("SERVER_HOST"))

    def generate_scaffold_pys(self, package_dir: Path, models_dir: Path):
        super().generate_scaffold_pys(package_dir, models_dir)
        update_file(
            Path(package_dir, "http_utils.py"),
            get_existing_content(
                Path(Path(servey_stub.__file__).parent, "templates", "http_utils.py")
            ),
        )

    def create_models(
        self, model_dir: Path, model_package_name: str
    ) -> Tuple[ImportsDefinition, TypeDefinitionContext]:
        imports, type_definition_context = super().create_models(
            model_dir, model_package_name
        )
        imports.add(["marshy"])
        imports.add([self.service_name, "http_utils"])
        imports = imports.optimize()
        return imports, type_definition_context

    def write_function_body(
        self,
        action: Action,
        sig: inspect.Signature,
        context: TypeDefinitionContext,
        writer: IOBase,
    ):
        trigger = next(t for t in action.triggers if isinstance(t, WebTrigger))
        writer.write("        event_ = {\n")
        for param in sig.parameters.values():
            writer.write('            "')
            writer.write(param.name)
            writer.write('": marshy.dump(')
            writer.write(param.name)
            writer.write(", ")
            type_name = getattr(param.annotation, "__name__", None) or str(
                param.annotation
            )
            writer.write(type_name)
            writer.write("),\n")
        writer.write("        }\n")
        writer.write('        result_ = http_utils.invoke("')
        url = self.service_root_url + (
            trigger.path or ("/" + action.name.replace("_", "-"))
        )
        writer.write(url)
        writer.write('", "')
        writer.write(trigger.method.value)
        writer.write('", event_, ')
        writer.write(str(action.timeout))
        writer.write(")\n")
        writer.write(
            "        loaded_result_ = marshy.load(result_)\n        return loaded_result_\n\n"
        )

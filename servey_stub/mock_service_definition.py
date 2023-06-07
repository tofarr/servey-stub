import inspect
import json
from dataclasses import dataclass
from io import IOBase
from pathlib import Path
from typing import Tuple

from marshy.types import ExternalItemType
from servey.action.action import Action

import servey_stub
from servey_stub.service_definition_abc import ServiceDefinitionABC
from servey_stub.type_definition.imports_definition import ImportsDefinition
from servey_stub.type_definition.type_definition_context import TypeDefinitionContext
from servey_stub.utils import get_existing_content, update_file


@dataclass
class MockServiceDefinition(ServiceDefinitionABC):
    def generate_scaffold_pys(self, package_dir: Path, models_dir: Path):
        super().generate_scaffold_pys(package_dir, models_dir)
        update_file(
            Path(package_dir, "mock_utils.py"),
            get_existing_content(
                Path(Path(servey_stub.__file__).parent, "templates", "mock_utils.py")
            ),
        )

    def create_models(
        self, model_dir: Path, model_package_name: str
    ) -> Tuple[ImportsDefinition, TypeDefinitionContext]:
        imports, type_definition_context = super().create_models(
            model_dir, model_package_name
        )
        imports.add(["marshy"])
        imports.add([self.service_name, "mock_utils"])
        imports = imports.optimize()
        return imports, type_definition_context

    def gather_examples(self) -> ExternalItemType:
        examples = {}
        for action in self.actions:
            examples[action.name] = [
                [example.params, example.result] for example in (action.examples or [])
            ]
        return examples

    def write_class_header(self, writer: IOBase):
        writer.write("\n\nMOCKS = ")
        json.dump(self.gather_examples(), writer)
        writer.write("\n\n\n")
        writer.write("class ")
        writer.write("".join(s.title() for s in self.service_name.split("_")))
        writer.write(":\n\n")

    def write_function_body(
        self,
        action: Action,
        sig: inspect.Signature,
        context: TypeDefinitionContext,
        writer: IOBase,
    ):
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
        writer.write('        result_ = mock_utils.get_mock_result("')
        writer.write(action.name)
        writer.write('", event_, MOCKS)\n')
        writer.write(
            "        loaded_result_ = marshy.load(result_)\n        return loaded_result_\n\n"
        )

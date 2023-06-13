import inspect
import json
import os
from abc import ABC, abstractmethod
from dataclasses import field, dataclass
from io import StringIO, IOBase
from pathlib import Path
from typing import List, Optional, Tuple

from servey.action.action import Action
from servey.finder.action_finder_abc import find_actions_with_trigger_type
from servey.trigger.web_trigger import WebTrigger
from servey.util import to_snake_case, get_servey_main

import servey_stub
from servey_stub.type_definition.imports_definition import ImportsDefinition
from servey_stub.type_definition.type_definition_context import TypeDefinitionContext
from servey_stub.utils import update_file, read_file


@dataclass
class ServiceDefinitionABC(ABC):
    actions: List[Action] = field(
        default_factory=lambda: [
            action for action, trigger in find_actions_with_trigger_type(WebTrigger)
        ]
    )
    service_name: str = field(default_factory=get_servey_main)
    output_dir: Path = Path("servey_stub")
    description: Optional[str] = field(
        default_factory=lambda: os.environ.get("SERVEY_API_DESCRIPTION")
    )
    version: str = field(
        default_factory=lambda: os.environ.get("SERVEY_API_VERSION") or "0.1.0"
    )
    install_requires: List[str] = field(default_factory=lambda: ["marshy"])

    @property
    def service_type_name(self):
        return "".join(
            to_snake_case(self.__class__.__name__).split("_service_definition")
        )

    def create_models(
        self, model_dir: Path, model_package_name: str
    ) -> Tuple[ImportsDefinition, TypeDefinitionContext]:
        imports = ImportsDefinition()
        context = TypeDefinitionContext(
            model_dir=model_dir, model_package_name=model_package_name
        )
        for type_ in _get_types_for_actions(self.actions):
            type_definition = context.get_type_definition(type_)
            if type_definition.imports:
                imports.add_all(type_definition.imports)
        imports = imports.optimize()
        return imports, context

    def generate_service_code(self):
        service_name = to_snake_case(self.service_name)
        project_dir, package_dir, models_dir = self.generate_directories(service_name)
        self.generate_scaffold_pys(package_dir, models_dir)
        imports, context = self.create_models(models_dir, service_name + ".models")
        self.generate_service_py(package_dir, service_name, imports, context)
        self.generate_setup_py(project_dir, service_name)

    def generate_directories(self, service_name: str) -> Tuple[Path, Path, Path]:
        project_dir = Path(self.output_dir, service_name + "_" + self.service_type_name)
        package_dir = Path(project_dir, service_name)
        models_dir = Path(package_dir, "models")
        models_dir.mkdir(parents=True, exist_ok=True)
        return project_dir, package_dir, models_dir

    def generate_scaffold_pys(self, package_dir: Path, models_dir: Path):
        update_file(Path(package_dir, "__init__.py"), "")
        update_file(Path(models_dir, "__init__.py"), "")

    def generate_setup_py(self, project_dir: Path, service_name: str):
        setup_content = read_file(
            Path(Path(servey_stub.__file__).parent, "templates", "setup.txt")
        )
        setup_content = setup_content.format(
            service_name=service_name,
            version=self.version,
            install_requires=self.install_requires,
        )
        update_file(Path(project_dir, "setup.py"), setup_content)

    def generate_service_py(
        self,
        package_dir: str,
        service_name: str,
        imports: ImportsDefinition,
        context: TypeDefinitionContext,
    ):
        writer = StringIO()
        self.write(imports, context, writer)
        service_content = writer.getvalue()
        service_file = Path(package_dir, service_name + ".py")
        update_file(service_file, service_content)

    def write(
        self, imports: ImportsDefinition, context: TypeDefinitionContext, writer: IOBase
    ):
        imports.write(writer)
        self.write_class_header(writer)
        for action in self.actions:
            self.write_action(action, context, writer)

    def write_class_header(self, writer: IOBase):
        writer.write("\n\n")
        writer.write("class ")
        writer.write("".join(s.title() for s in self.service_name.split("_")))
        writer.write(":\n\n")

    def write_action(
        self, action: Action, context: TypeDefinitionContext, writer: IOBase
    ):
        sig = inspect.signature(action.fn)
        self.write_function_header(action, sig, context, writer)
        self.write_function_body(action, sig, context, writer)
        writer.write("\n")

    @staticmethod
    def write_function_header(
        action: Action,
        sig: inspect.Signature,
        context: TypeDefinitionContext,
        writer: IOBase,
    ):
        writer.write("    def ")
        writer.write(action.name)
        writer.write("(self")
        for param in sig.parameters.values():
            writer.write(", ")
            writer.write(param.name)
            writer.write(": ")
            writer.write(context.type_definitions[param.annotation].type_name)
            if param.default is not sig.empty:
                writer.write(" = ")
                if isinstance(param.default, str):
                    writer.write(json.dumps(param.default))
                else:
                    writer.write(str(param.default))
        writer.write("):\n")

    @abstractmethod
    def write_function_body(
        self,
        action: Action,
        sig: inspect.Signature,
        context: TypeDefinitionContext,
        writer: IOBase,
    ):
        """Write the body of a function"""


def _get_types_for_actions(actions: List[Action]):
    for action in actions:
        sig = inspect.signature(action.fn)
        for param in sig.parameters.values():
            yield param.annotation
        yield sig.return_annotation

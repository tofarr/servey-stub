import inspect
import json
from dataclasses import dataclass
from enum import Enum
from io import StringIO, IOBase
from typing import Type, Optional

from servey.util import to_snake_case

from servey_stub.type_definition.imports_definition import ImportsDefinition
from servey_stub.type_definition.type_definition import TypeDefinition
from servey_stub.type_definition.type_definition_context import TypeDefinitionContext
from servey_stub.type_definition.type_definition_factory_abc import (
    TypeDefinitionFactoryABC,
)
from servey_stub.utils import update_file


@dataclass
class EnumTypeDefinitionFactory(TypeDefinitionFactoryABC):
    priority: int = 110

    def create_type_definition(
        self, type_: Type, context: TypeDefinitionContext
    ) -> Optional[TypeDefinition]:
        if not inspect.isclass(type_) or not issubclass(type_, Enum):
            return
        name = type_.__name__
        type_definition = TypeDefinition(
            name,
            ImportsDefinition(
                [context.model_package_name + "." + to_snake_case(name) + "." + name]
            ),
        )
        model_file = context.model_dir / (to_snake_case(name) + ".py")
        writer = StringIO()
        self.write_enum_definition(type_, writer)
        update_file(model_file, writer.getvalue())
        return type_definition

    @staticmethod
    def write_enum_definition(type_: Type, writer: IOBase):
        writer.write("from enum import Enum\n\nclass ")
        writer.write(type_.__name__)
        writer.write("(Enum):\n")
        for e in type_:
            writer.write("    ")
            writer.write(e.name)
            writer.write(" = ")
            writer.write(json.dumps(e.value))
            writer.write("\n")

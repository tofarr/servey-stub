from dataclasses import dataclass, field
from datetime import datetime
from typing import Type, Dict, Optional
from uuid import UUID

from servey_stub.type_definition.imports_definition import ImportsDefinition
from servey_stub.type_definition.type_definition import TypeDefinition
from servey_stub.type_definition.type_definition_context import TypeDefinitionContext
from servey_stub.type_definition.type_definition_factory_abc import (
    TypeDefinitionFactoryABC,
)


def get_type_definitions() -> Dict[Type, TypeDefinition]:
    return {
        bool: TypeDefinition(bool.__name__),
        float: TypeDefinition(float.__name__),
        int: TypeDefinition(int.__name__),
        str: TypeDefinition(str.__name__),
        UUID: TypeDefinition(UUID.__name__, ImportsDefinition(["uuid.UUID"])),
        datetime: TypeDefinition(
            datetime.__name__, ImportsDefinition(["datetime.datetime"])
        ),
    }


@dataclass
class PrimitiveTypeDefinitionFactory(TypeDefinitionFactoryABC):
    priority: int = 110
    type_definitions: Dict[Type, TypeDefinition] = field(
        default_factory=get_type_definitions
    )

    def create_type_definition(
        self, type_: Type, context: TypeDefinitionContext
    ) -> Optional[TypeDefinition]:
        type_definition = self.type_definitions.get(type_)
        if type_definition:
            return type_definition

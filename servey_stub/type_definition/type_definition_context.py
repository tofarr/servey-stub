from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Type

from marshy.factory.impl_marshaller_factory import get_impls

from servey_stub.errors import StubError
from servey_stub.type_definition.type_definition import TypeDefinition
from servey_stub.type_definition.type_definition_factory_abc import (
    TypeDefinitionFactoryABC,
)


def get_type_definition_factories():
    result = [i() for i in get_impls(TypeDefinitionFactoryABC)]
    result.sort(key=lambda t: t.priority)
    return result


@dataclass
class TypeDefinitionContext:
    model_dir: Path
    model_package_name: str
    type_definition_factories: List[TypeDefinitionFactoryABC] = field(
        default_factory=get_type_definition_factories
    )
    type_definitions: Dict[Type, TypeDefinition] = field(default_factory=dict)

    def get_type_definition(self, type_: Type) -> TypeDefinition:
        type_definition = self.type_definitions.get(type_)
        if type_definition:
            return type_definition
        for factory in self.type_definition_factories:
            type_definition = factory.create_type_definition(type_, self)
            if type_definition:
                self.type_definitions[type_] = type_definition
                return type_definition
        raise StubError(f"no_definition_for_type:{type_}")

from typing import Type, Optional, ForwardRef

import typing_inspect
from marshy.utils import resolve_forward_refs

from servey_stub.type_definition.imports_definition import ImportsDefinition
from servey_stub.type_definition.type_definition import TypeDefinition
from servey_stub.type_definition.type_definition_context import TypeDefinitionContext
from servey_stub.type_definition.type_definition_factory_abc import (
    TypeDefinitionFactoryABC,
)


class ForwardRefDefinitionFactory(TypeDefinitionFactoryABC):
    def create_type_definition(
        self, type_: Type, context: TypeDefinitionContext
    ) -> Optional[TypeDefinition]:
        if getattr(type_, "__class__", None) != ForwardRef:
            return

        resolved = resolve_forward_refs(type_)
        type_definition = context.get_type_definition(resolved)

        imports = ImportsDefinition()
        imports.add("typing.ForwardRef")
        ref = ".".join(type_definition.imports.imports[0])
        return TypeDefinition(f"ForwardRef(\"{ref}\")", imports)

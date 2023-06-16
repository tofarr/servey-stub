from typing import Type, Optional

import typing_inspect

from servey_stub.type_definition.imports_definition import ImportsDefinition
from servey_stub.type_definition.type_definition import TypeDefinition
from servey_stub.type_definition.type_definition_context import TypeDefinitionContext
from servey_stub.type_definition.type_definition_factory_abc import (
    TypeDefinitionFactoryABC,
)


class GenericTypeDefinitionFactory(TypeDefinitionFactoryABC):
    def create_type_definition(
        self, type_: Type, context: TypeDefinitionContext
    ) -> Optional[TypeDefinition]:
        origin = typing_inspect.get_origin(type_)
        if not origin:
            return
        name = str(type_)
        imports = ImportsDefinition()
        if name.startswith("typing."):
            prefix = name.split("[", maxsplit=1)[0]
            imports.add(prefix)
            arg_names = []
            for arg in typing_inspect.get_args(type_):
                if arg is not type(None):
                    arg_type_definition = context.get_type_definition(arg)
                    arg_names.append(arg_type_definition.type_name)
                    if arg_type_definition.imports:
                        imports.add_all(arg_type_definition.imports)
            type_name = f"{prefix}[{', '.join(arg_names)}]"
            return TypeDefinition(type_name, imports)

from abc import ABC, abstractmethod
from typing import Type, Optional

from servey_stub.type_definition.type_definition import TypeDefinition

_TypeDefinitionContext = (
    "servey_stub.type_definition.type_definition_context.TypeDefinitionContext"
)


class TypeDefinitionFactoryABC(ABC):
    priority: int = 100

    @abstractmethod
    def create_type_definition(
        self, type_: Type, context: _TypeDefinitionContext
    ) -> Optional[TypeDefinition]:
        """Generate a type name and return it, (and generate any additional required model files)"""

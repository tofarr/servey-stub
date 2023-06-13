from marshy.factory.impl_marshaller_factory import register_impl
from marshy.marshaller_context import MarshallerContext

from servey_stub.type_definition.dataclass_type_definition_factory import (
    DataclassTypeDefinitionFactory,
)
from servey_stub.type_definition.enum_type_definition_factory import (
    EnumTypeDefinitionFactory,
)
from servey_stub.type_definition.generic_type_definition_factory import (
    GenericTypeDefinitionFactory,
)
from servey_stub.type_definition.primitive_type_definition_factory import (
    PrimitiveTypeDefinitionFactory,
)
from servey_stub.type_definition.type_definition_factory_abc import (
    TypeDefinitionFactoryABC,
)

priority = 100


def configure(context: MarshallerContext):
    register_impl(TypeDefinitionFactoryABC, DataclassTypeDefinitionFactory, context)
    register_impl(TypeDefinitionFactoryABC, PrimitiveTypeDefinitionFactory, context)
    register_impl(TypeDefinitionFactoryABC, EnumTypeDefinitionFactory, context)
    register_impl(TypeDefinitionFactoryABC, GenericTypeDefinitionFactory, context)

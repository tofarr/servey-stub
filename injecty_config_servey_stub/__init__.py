from injecty import InjectyContext

from servey_stub.type_definition.dataclass_type_definition_factory import (
    DataclassTypeDefinitionFactory,
)
from servey_stub.type_definition.enum_type_definition_factory import (
    EnumTypeDefinitionFactory,
)
from servey_stub.type_definition.forward_ref_definition_factory import (
    ForwardRefDefinitionFactory,
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


def configure(context: InjectyContext):
    context.register_impls(
        TypeDefinitionFactoryABC,
        [
            DataclassTypeDefinitionFactory,
            PrimitiveTypeDefinitionFactory,
            EnumTypeDefinitionFactory,
            GenericTypeDefinitionFactory,
            ForwardRefDefinitionFactory,
        ],
    )

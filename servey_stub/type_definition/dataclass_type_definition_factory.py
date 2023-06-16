import json
from dataclasses import is_dataclass, fields, MISSING
from io import StringIO
from pathlib import Path
from typing import Type, Optional

from marshy import ExternalType
from servey.util import to_snake_case

from servey_stub.type_definition.dataclass_definition import DataclassDefinition
from servey_stub.type_definition.field_definition import FieldDefinition
from servey_stub.type_definition.imports_definition import ImportsDefinition
from servey_stub.type_definition.type_definition import TypeDefinition
from servey_stub.type_definition.type_definition_context import TypeDefinitionContext
from servey_stub.type_definition.type_definition_factory_abc import (
    TypeDefinitionFactoryABC,
)
from servey_stub.utils import update_file


class DataclassTypeDefinitionFactory(TypeDefinitionFactoryABC):
    def create_type_definition(
        self, type_: Type, context: TypeDefinitionContext
    ) -> Optional[TypeDefinition]:
        if not is_dataclass(type_):
            return
        name = type_.__name__
        snake_name = to_snake_case(name)
        model_package_name = f"{context.model_package_name}.{snake_name}.{name}"
        type_definition = TypeDefinition(
            name, ImportsDefinition([model_package_name.split(".")])
        )
        context.type_definitions[type_] = type_definition  # Prevent recursion
        model_file = Path(context.model_dir, (snake_name + ".py"))
        dataclass_definition = self.create_dataclass_definition(type_, context)
        writer = StringIO()
        dataclass_definition.write(writer)
        update_file(model_file, writer.getvalue())
        return type_definition

    @staticmethod
    def create_dataclass_definition(
        type_: Type, context: TypeDefinitionContext
    ) -> DataclassDefinition:
        imports = ImportsDefinition([["dataclasses", "dataclass"]])
        field_definitions = []
        # noinspection PyDataclass
        for field in fields(type_):
            field_type_definition = context.get_type_definition(field.type)
            if field_type_definition.imports:
                imports.add_all(field_type_definition.imports)
            schema = field.metadata.get("schemey")
            if schema and not has_ref(schema.schema):
                schema = schema.schema
                imports.add("schemey.schema_from_json")
            else:
                schema = None
            field_definition = FieldDefinition(
                name=field.name,
                type=field_type_definition.type_name,
                default_value=default_value_to_str(field),
                schema=schema,
            )
            field_definitions.append(field_definition)
        imports = imports.optimize()
        dataclass_definition = DataclassDefinition(
            name=type_.__name__,
            imports=imports,
            fields=field_definitions,
        )
        return dataclass_definition


def default_value_to_str(field):
    if field.default is MISSING:
        return None
    if field.default in (True, False, None):
        return str(field.default)
    return json.dumps(field.default)


def has_ref(schema: ExternalType) -> bool:
    if isinstance(schema, dict):
        if schema.get("$ref"):
            return True
        for s in schema.values():
            if has_ref(s):
                return True
    elif isinstance(schema, list):
        for s in schema:
            if has_ref(s):
                return True
    return False

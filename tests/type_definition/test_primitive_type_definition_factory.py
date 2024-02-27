from datetime import datetime
from typing import Type, Optional
from unittest import TestCase
from uuid import UUID

from servey_stub.type_definition.imports_definition import ImportsDefinition
from servey_stub.type_definition.primitive_type_definition_factory import (
    PrimitiveTypeDefinitionFactory,
)
from servey_stub.type_definition.type_definition import TypeDefinition


class TestPrimitiveTypeDefinitionFactory(TestCase):
    def test_create_type_definition_bool(self):
        self._create_type_definition(bool)

    def test_create_type_definition_datetime(self):
        self._create_type_definition(datetime, ImportsDefinition([["datetime", "datetime"]]))

    def test_create_type_definition_float(self):
        self._create_type_definition(float)

    def test_create_type_definition_int(self):
        self._create_type_definition(int)

    def test_create_type_definition_str(self):
        self._create_type_definition(str)

    def test_create_type_definition_uuid(self):
        self._create_type_definition(UUID, ImportsDefinition([["uuid", "UUID"]]))

    def _create_type_definition(
        self, type_: Type, imports: Optional[ImportsDefinition] = None
    ):
        factory = PrimitiveTypeDefinitionFactory()
        type_definition = factory.create_type_definition(type_, None)
        expected = TypeDefinition(type_.__name__, imports)
        self.assertEqual(type_definition, expected)

    def test_create_type_definition_unknown(self):
        factory = PrimitiveTypeDefinitionFactory()
        type_definition = factory.create_type_definition(
            TestPrimitiveTypeDefinitionFactory, None
        )
        self.assertIsNone(type_definition)

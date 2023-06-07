from io import StringIO
from unittest import TestCase

from schemey.schema import str_schema

from servey_stub.type_definition.field_definition import FieldDefinition


class TestFieldDefinition(TestCase):
    def test_write_with_schema_and_default(self):
        field_definition = FieldDefinition(
            "foo", "str", '"bar"', str_schema(max_length=64).schema
        )
        writer = StringIO()
        field_definition.write(writer)
        expected = '    foo: str = field(default="bar", metadata={"schemey": {"type": "string", "maxLength": 64}})\n'
        value = writer.getvalue()
        self.assertEqual(expected, value)

    def test_write_with_schema(self):
        field_definition = FieldDefinition(
            "foo", "str", None, str_schema(max_length=64).schema
        )
        writer = StringIO()
        field_definition.write(writer)
        expected = '    foo: str = field(metadata={"schemey": {"type": "string", "maxLength": 64}})\n'
        value = writer.getvalue()
        self.assertEqual(expected, value)

    def test_write_with_default(self):
        field_definition = FieldDefinition("foo", "str", '"bar"')
        writer = StringIO()
        field_definition.write(writer)
        expected = '    foo: str = "bar"\n'
        value = writer.getvalue()
        self.assertEqual(expected, value)

    def test_write(self):
        field_definition = FieldDefinition("foo", "str")
        writer = StringIO()
        field_definition.write(writer)
        expected = "    foo: str\n"
        value = writer.getvalue()
        self.assertEqual(expected, value)

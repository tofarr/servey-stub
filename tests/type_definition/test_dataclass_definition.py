from dataclasses import dataclass
from io import StringIO
from unittest import TestCase

from servey_stub.type_definition.dataclass_definition import DataclassDefinition
from servey_stub.type_definition.field_definition import FieldDefinition
from servey_stub.type_definition.imports_definition import ImportsDefinition


class TestDataclassDefinition(TestCase):
    def test_write(self):
        dataclass_definition = DataclassDefinition(
            name="ZapBang",
            imports=ImportsDefinition([["ping", "pong"]]),
            fields=[
                FieldDefinition("zap", "int"),
                FieldDefinition("bang", "bool", "True"),
            ],
            description="A Zap Bang!",
        )
        writer = StringIO()
        dataclass_definition.write(writer)
        value = writer.getvalue().split("\n")
        self.assertEqual(value, EXPECTED_VALUE)


EXPECTED_VALUE = [
    "from ping import pong",
    "",
    "",
    "@dataclass",
    "class ZapBang:",
    '    """A Zap Bang!    """',
    "    zap: int",
    "    bang: bool = True",
    "",
]

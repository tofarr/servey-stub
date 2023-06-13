from dataclasses import MISSING
from pathlib import Path
from unittest import TestCase

from servey_stub.errors import StubError
from servey_stub.type_definition.type_definition_context import TypeDefinitionContext


class TestTypeDefinitionContext(TestCase):
    def test_no_definition(self):
        context = TypeDefinitionContext(Path("models"), "models")
        with self.assertRaises(StubError):
            context.get_type_definition(MISSING)

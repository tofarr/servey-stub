from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List
from unittest import TestCase
from unittest.mock import patch

from schemey.schema import str_schema
from schemey.string_format import StringFormat

from servey_stub.type_definition.dataclass_type_definition_factory import (
    DataclassTypeDefinitionFactory,
    has_ref,
    default_value_to_str,
)
from servey_stub.type_definition.imports_definition import ImportsDefinition
from servey_stub.type_definition.type_definition import TypeDefinition
from servey_stub.type_definition.type_definition_context import TypeDefinitionContext
from tests.mock_file_system import MockFileSystem


class TestEnumTypeDefinitionFactory(TestCase):
    def test_create_type_definition(self):
        context = TypeDefinitionContext(Path("my_project/models"), "my_project.models")
        factory = DataclassTypeDefinitionFactory()
        mock_file_system = MockFileSystem()
        # noinspection SpellCheckingInspection
        with (
            patch("os.path.exists", mock_file_system.exists),
            patch("builtins.open", mock_file_system.open),
            patch("pathlib.PosixPath.mkdir", mock_file_system.mkdir),
        ):
            type_definition = factory.create_type_definition(FooBar, context)
            type_definition_2 = factory.create_type_definition(FooBar, context)
        self.assertEqual(
            type_definition,
            TypeDefinition(
                "FooBar",
                ImportsDefinition([["my_project", "models", "foo_bar", "FooBar"]]),
            ),
        )
        self.assertEqual(type_definition, type_definition_2)
        self.assertEqual(1, len(mock_file_system.contents))
        content = (
            mock_file_system.contents.get(Path("my_project/models/foo_bar.py"))
            .getvalue()
            .split("\n")
        )
        next(c for c in content if c.startswith("# Updated At: "))
        content = [c for c in content if not c.startswith("# Updated At: ")]
        self.assertEqual(DATACLASS_CONTENT, content)

    def test_create_type_definition_unknown(self):
        context = TypeDefinitionContext(Path("my_project/models"), "my_project.models")
        factory = DataclassTypeDefinitionFactory()
        type_definition = factory.create_type_definition(
            TestEnumTypeDefinitionFactory, context
        )
        self.assertIsNone(type_definition)

    def test_create_type_definition_nested(self):
        context = TypeDefinitionContext(Path("my_project/models"), "my_project.models")
        factory = DataclassTypeDefinitionFactory()
        mock_file_system = MockFileSystem()
        # noinspection SpellCheckingInspection
        with (
            patch("os.path.exists", mock_file_system.exists),
            patch("builtins.open", mock_file_system.open),
            patch("pathlib.PosixPath.mkdir", mock_file_system.mkdir),
        ):
            type_definition = factory.create_type_definition(ZapBang, context)
        self.assertEqual(
            type_definition,
            TypeDefinition(
                "ZapBang",
                ImportsDefinition([["my_project", "models", "zap_bang", "ZapBang"]]),
            ),
        )
        self.assertEqual(2, len(mock_file_system.contents))
        contents = {
            str(k): [s for s in v.getvalue().split("\n") if not s.startswith("#")]
            for k, v in mock_file_system.contents.items()
            if "/templates/" not in str(k)
        }
        expected_contents = {
            "my_project/models/foo_bar.py": [
                "from dataclasses import dataclass, field",
                "from schemey import schema_from_json",
                "from typing import Optional",
                "",
                "",
                "@dataclass",
                "class FooBar:",
                "    foo: str",
                "    bar: bool = True",
                "    email: Optional[str] = field(default=None, "
                'metadata={"schemey": schema_from_json({"type": "string", "maxLength": 255, "format": "email"})})',
                "",
            ],
            "my_project/models/zap_bang.py": [
                "from dataclasses import dataclass",
                "from my_project.models.foo_bar import FooBar",
                "from typing import List",
                "",
                "",
                "@dataclass",
                "class ZapBang:",
                "    title: str",
                "    foobars: List[FooBar]",
                "",
            ],
        }
        self.assertEqual(expected_contents, contents)

    def test_has_ref(self):
        self.assertFalse(has_ref("foobar"))
        self.assertTrue(has_ref({"ping": [10, False, {"$ref": "#/foo/bar"}]}))

    def test_default_value_to_str(self):
        self.assertEqual('"foo"', default_value_to_str(field(default="foo")))
        self.assertEqual("10", default_value_to_str(field(default=10)))
        self.assertEqual("True", default_value_to_str(field(default=True)))


@dataclass
class FooBar:
    foo: str
    bar: bool = True
    email: Optional[str] = field(
        default=None,
        metadata={"schemey": str_schema(max_length=255, str_format=StringFormat.EMAIL)},
    )


@dataclass
class ZapBang:
    title: str
    foobars: List[FooBar] = field(default_factory=list)


DATACLASS_CONTENT = [
    "# GENERATED BY SERVEY-STUB",
    "# Manual updates to this file may be lost. ",
    "from dataclasses import dataclass, field",
    "from schemey import schema_from_json",
    "from typing import Optional",
    "",
    "",
    "@dataclass",
    "class FooBar:",
    "    foo: str",
    "    bar: bool = True",
    '    email: Optional[str] = field(default=None, metadata={"schemey": '
    'schema_from_json({"type": "string", "maxLength": 255, "format": "email"})})',
    "",
]

from io import StringIO
from unittest import TestCase

from servey_stub.type_definition.imports_definition import ImportsDefinition


class TestImportsDefinition(TestCase):
    def test_add(self):
        imports = ImportsDefinition()
        imports.add("foo.bar.Zap")
        imports.add("foo.bar.Bang")
        string = StringIO()
        imports.write(string)
        import_str = string.getvalue()
        expected_import_str = "from foo.bar import Zap\nfrom foo.bar import Bang\n"
        self.assertEqual(import_str, expected_import_str)

    def test_optimize(self):
        imports = ImportsDefinition()
        imports.add("foo.bar.zap.Bang")
        imports.add("foo.bar.zap.Fizz")
        imports.add("foo.bar.fizz.Buzz")
        imports.add("foo.bar.ping.Pong")
        imports = imports.optimize()
        string = StringIO()
        imports.write(string)
        import_str = string.getvalue()
        expected_import_str = "".join(
            [
                "from foo.bar.fizz import Buzz\n",
                "from foo.bar.ping import Pong\n",
                "from foo.bar.zap import Bang, Fizz\n",
            ]
        )
        self.assertEqual(import_str, expected_import_str)

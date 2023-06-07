from dataclasses import dataclass, field
from io import IOBase
from typing import Optional, List

from servey_stub.type_definition.field_definition import FieldDefinition
from servey_stub.type_definition.imports_definition import ImportsDefinition


def _default_dataclass_imports():
    return ImportsDefinition([["dataclasses", "dataclass"]])


@dataclass
class DataclassDefinition:
    """
    Definition for code generation for a dataclass to be used as a data transfer object
    """

    name: str
    imports: ImportsDefinition = field(default_factory=_default_dataclass_imports)
    fields: List[FieldDefinition] = field(default_factory=list)
    description: Optional[str] = None

    def write(self, writer: IOBase):
        self.imports.write(writer)
        writer.write("\n\n@dataclass\nclass ")
        writer.write(self.name)
        writer.write(":\n")
        if self.description:
            writer.write('    """')
            writer.write(self.description.replace("\n", "\n    "))
            writer.write('    """\n')
        for field in self.fields:
            field.write(writer)

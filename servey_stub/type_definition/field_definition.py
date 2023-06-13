import json
from dataclasses import dataclass
from io import IOBase
from typing import Optional

from marshy.types import ExternalItemType


@dataclass
class FieldDefinition:
    name: str
    type: str
    default_value: Optional[str] = None
    schema: Optional[ExternalItemType] = None

    def write(self, writer: IOBase):
        writer.write("    ")
        writer.write(self.name)
        writer.write(": ")
        writer.write(self.type)
        if self.schema:
            writer.write(" = field(")
            if self.default_value is not None:
                writer.write("default=")
                writer.write(self.default_value)
                writer.write(", ")
            writer.write('metadata={"schemey": schema_from_json(')
            json.dump(self.schema, writer)
            writer.write(")})")
        elif self.default_value is not None:
            writer.write(" = ")
            writer.write(self.default_value)
        writer.write("\n")

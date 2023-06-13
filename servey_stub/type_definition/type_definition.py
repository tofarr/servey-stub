from dataclasses import dataclass
from typing import Optional

from servey_stub.type_definition.imports_definition import ImportsDefinition


@dataclass
class TypeDefinition:
    type_name: str
    imports: Optional[ImportsDefinition] = None

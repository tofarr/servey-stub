from dataclasses import dataclass
from typing import Optional


@dataclass
class TypeDefinition:
    type_name: str
    import_name: Optional[str] = None

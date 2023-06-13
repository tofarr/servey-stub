from __future__ import annotations
from dataclasses import dataclass, field
from io import IOBase
from typing import List, Union


@dataclass
class ImportsDefinition:
    imports: List[List[str]] = field(default_factory=list)

    def add(self, path: Union[str, List[str]]):
        if isinstance(path, str):
            path = path.split(".")
        self.imports.append(path)

    def add_all(self, imports: ImportsDefinition):
        self.imports.extend(imports.imports)

    def optimize(self) -> ImportsDefinition:
        root_imports = set()
        optimized_imports = {}
        for type_import in self.imports:
            key = tuple(type_import[:-1])
            values = set(s.strip() for s in type_import[-1].split(","))
            if key:
                existing = optimized_imports.get(key)
                if existing:
                    existing.update(values)
                else:
                    optimized_imports[key] = values
            else:
                root_imports.add(tuple(values))
        imports = list(list(i) for i in root_imports)
        for key, value in optimized_imports.items():
            type_import = list(key)
            value = list(value)
            value.sort()
            type_import.append(", ".join(value))
            imports.append(type_import)
        imports.sort()
        return ImportsDefinition(imports)

    def write(self, writer: IOBase):
        for type_import in self.imports:
            if len(type_import) > 1:
                writer.write("from ")
                writer.write(".".join(type_import[:-1]))
                writer.write(" ")
            writer.write("import ")
            writer.write(type_import[-1])
            writer.write("\n")

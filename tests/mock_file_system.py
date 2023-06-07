from dataclasses import dataclass, field
from io import StringIO
from typing import Dict


@dataclass
class MockFileSystem:
    contents: Dict[str, StringIO] = field(default_factory=dict)

    def mkdir(self, parents: bool, exist_ok: bool):
        pass

    def exists(self, path):
        return path in self.contents

    def open(self, path: str, mode: str):
        if mode == "r":
            result = self.contents[path]
            return result
        elif mode == "w":
            result = self.contents[path] = ResetOnCloseStringIO()
            return result


class ResetOnCloseStringIO(StringIO):
    def close(self):
        self.seek(0)

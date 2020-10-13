from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class TagSpaceEntry:
    file: Optional[Path] = None
    configFile: Optional[Path] = None

    def __post_init__(self):
        if not self.configFile.exists():
            self.configFile = None

    def isValid(self):
        return (self.file is not None
                and self.configFile is not None)

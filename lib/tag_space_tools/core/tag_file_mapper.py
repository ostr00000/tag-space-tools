from pathlib import Path
from typing import Union

from tag_space_tools.core.file_searcher import TagSpaceSearcher


class TagFileMapper(TagSpaceSearcher):
    def __init__(self, location: Union[Path, str]):
        super().__init__(location)
        del self.missingTagConfigs
        del self.missingTagFiles

    def getTagEntryInDir(self, dirPath: Path, recursive=True):
        if recursive:
            return [te for te in self.validTagEntries if te.file.is_relative_to(dirPath)]
        else:
            return [te for te in self.validTagEntries if te.file.parent == dirPath]

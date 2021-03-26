from os import PathLike
from pathlib import Path
from typing import List, Iterable, Optional

from tag_space_tools.core.file_searcher import TagSpaceSearcher
from tag_space_tools.core.tag_space_entry import TagSpaceEntry


class TagFinder:
    def __init__(self, path: PathLike):
        self.tss = TagSpaceSearcher(path)

    def findAllTags(self) -> List[str]:
        tags = set()
        for vte in self.tss.validTagEntries:
            tags.update(vte.tags)

        return sorted(t.title for t in tags)

    def genFilesWithTag(self, tagName: str,
                        extensions: Optional[list[str]] = None
                        ) -> Iterable[Path]:
        if extensions is not None:
            extensions = [e if e.startswith('.') else e + '.' for e in extensions]

        for tagEntry in self.genEntriesWithTag(tagName):
            if extensions is None or tagEntry.file.suffix in extensions:
                yield tagEntry.file

    def genEntriesWithTag(self, tagName: str) -> Iterable[TagSpaceEntry]:
        for tagEntry in self.tss.validTagEntries:
            if tagName in tagEntry.tags:
                yield tagEntry

    def getAllTagEntries(self):
        return self.tss.validTagEntries

    def getTagEntryInDir(self, dirPath: PathLike, recursive=True):
        if recursive:
            return [te for te in self.tss.validTagEntries if te.file.is_relative_to(dirPath)]
        else:
            return [te for te in self.tss.validTagEntries if te.file.parent == dirPath]

    def getTagEntriesWithMissingConfig(self) -> Iterable[TagSpaceEntry]:
        for entries in self.tss.missingTagFiles.values():
            yield from entries

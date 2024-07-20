from collections.abc import Iterable
from pathlib import Path

from pyqt_utils.python.typing_const import StrPath
from pyqt_utils.widgets.tag_filter.nodes import TagFilterNode

from tag_space_tools.core.file_searcher import TagSpaceSearcher
from tag_space_tools.core.tag_space_entry import TagSpaceEntry


class TagFinder:
    def __init__(self, path: StrPath):
        self.tss = TagSpaceSearcher(path)

    def findAllTags(self) -> list[str]:
        tags = set()
        for vte in self.tss.validTagEntries:
            tags.update(vte.tags)

        return sorted(t.title for t in tags)

    def genFilesWithTag(
        self, tagName: str | TagFilterNode, extensions: list[str] | None = None
    ) -> Iterable[Path]:
        if extensions is not None:
            extensions = [e if e.startswith('.') else e + '.' for e in extensions]

        for tagEntry in self.genEntriesWithTag(tagName):
            if extensions is None or tagEntry.requireFile.suffix in extensions:
                yield tagEntry.requireFile

    def genEntriesWithTag(
        self, tagFilter: str | TagFilterNode
    ) -> Iterable[TagSpaceEntry]:
        if isinstance(tagFilter, str):
            tagFilter = TagFilterNode(tagFilter)

        for tagEntry in self.tss.validTagEntries:
            if tagFilter.isAccepted(tagEntry.tags):
                yield tagEntry

    def getAllTagEntries(self):
        return self.tss.validTagEntries

    def getTagEntryInDir(self, dirPath: StrPath, *, recursive=True):
        if recursive:
            return [
                t
                for t in self.tss.validTagEntries
                if t.requireFile.is_relative_to(dirPath)
            ]

        return [t for t in self.tss.validTagEntries if t.requireFile.parent == dirPath]

    def getTagEntriesWithMissingConfig(self) -> Iterable[TagSpaceEntry]:
        for entries in self.tss.missingTagFiles.values():
            yield from entries

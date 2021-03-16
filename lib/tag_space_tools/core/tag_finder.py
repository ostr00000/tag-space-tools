from pathlib import Path
from typing import List, Iterable, Union, Optional

from tag_space_tools import modulePath
from tag_space_tools.core.file_searcher import TagSpaceSearcher


class TagFinder:
    def __init__(self, path: Union[Path, str]):
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

        for tagEntry in self.tss.validTagEntries:
            if tagName in tagEntry.tags:
                if extensions is None or tagEntry.file.suffix in extensions:
                    yield tagEntry.file


def main():
    p = Path(modulePath).parent.parent / 'test'
    print(p)
    tagFinder = TagFinder(p)

    allTags = tagFinder.findAllTags()
    print(allTags)
    for tagName in allTags:
        print(f'Tag: {tagName}')
        for fileName in tagFinder.genFilesWithTag(tagName):
            print(fileName)


if __name__ == '__main__':
    main()

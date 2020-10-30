from pathlib import Path
from typing import List, Iterable

from tag_space_tools import modulePath
from tag_space_tools.core.fix_tagspace import TagSpaceSearch


def findAllTags(path: Path) -> List[str]:
    tss = TagSpaceSearch(path)
    tags = set()

    for vte in tss.validTagEntries:
        tags.update(vte.tags)

    return [t.title for t in tags]


def genFilesWithTag(path: Path, tagName: str) -> Iterable[Path]:
    tss = TagSpaceSearch(path)
    for tagEntry in tss.validTagEntries:
        if tagName in tagEntry.tags:
            yield tagEntry.file


def main():
    p = Path(modulePath).parent.parent / 'test'
    print(p)
    allTags = findAllTags(p)
    print(allTags)
    for tagName in allTags:
        print(f'Tag: {tagName}')
        for fileName in genFilesWithTag(p, tagName):
            print(fileName)


if __name__ == '__main__':
    main()

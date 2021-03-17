from pathlib import Path
from typing import List, Iterable, Union, Optional

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

    def getAllTagEntries(self):
        return self.tss.validTagEntries

    def getTagEntryInDir(self, dirPath: Path, recursive=True):
        if recursive:
            return [te for te in self.tss.validTagEntries if te.file.is_relative_to(dirPath)]
        else:
            return [te for te in self.tss.validTagEntries if te.file.parent == dirPath]


if __name__ == '__main__':
    def main():
        tf = TagFinder('./s')
        entries = tf.getAllTagEntries()
        e = entries[0]
        print(e)
        from pprint import pprint
        pprint(e.tags)

        ok = e.renameTag('sitting', 'sit')
        print(ok)
        if not ok:
            ok = e.renameTag('sit', 'sitting')
            print(ok)

        pprint(e.tags)


    main()

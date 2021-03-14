import logging
from pathlib import Path
from typing import Iterator, Union, Optional, Iterable, TypeVar, Tuple, Container

from tag_space_tools.core.tag_file_mapper import TagFileMapper
from tag_space_tools.core.tag_space_entry import Tag

logger = logging.getLogger(__name__)
T = TypeVar('T')


def _dirGen(sortTag: list[Tag], tags: list[Tag], destDir: Path) -> Iterator[Path]:
    curPath = destDir
    for st in sortTag:
        if st in tags:
            curPath = curPath / st.title
            yield curPath


def _nextValueGen(gen: Iterable[T]) -> Iterator[Tuple[T, Optional[T]]]:
    it = iter(gen)
    try:
        val = next(it)
    except StopIteration:
        return

    for nextVal in it:
        yield val, nextVal
        val = nextVal
    yield val, None


def sortFiles(sortTag: list[Tag],
              srcDir: Union[Path, str],
              destDir: Union[Path, str],
              maxFilesInDir=20,
              recursive=True,
              excludeDir: Container[Path] = (),
              tagFileMapper: TagFileMapper = None):
    """Move files and their tags from 'srcDir' to 'destDir'.
    If there are more than 'maxFilesInDir' then create subdirectory.
    Subdirectory name is chosen based on moving file tags and 'sortTag' argument.
    """
    destDir = Path(destDir)
    if tagFileMapper is None:
        tagFileMapper = TagFileMapper(destDir)

    for tagEntry in tagFileMapper.getTagEntryInDir(srcDir, recursive=recursive):

        lastDir = destDir
        dirGen = _dirGen(sortTag, tagEntry.tags, destDir)
        for lastDir, nextDir in _nextValueGen(dirGen):
            if nextDir and nextDir.exists():
                continue

            if lastDir in excludeDir:
                continue

            taggedFilesCount = len(tagFileMapper.getTagEntryInDir(lastDir, recursive=False))
            if taggedFilesCount < maxFilesInDir:
                tagEntry.move(lastDir)
                break
            elif taggedFilesCount == maxFilesInDir:
                tagEntry.move(lastDir)
                sortFiles(sortTag, lastDir, destDir, maxFilesInDir,
                          recursive=False, excludeDir=(lastDir,), tagFileMapper=tagFileMapper)
                break

        else:
            tagEntry.move(lastDir)

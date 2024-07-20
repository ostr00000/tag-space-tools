import logging
from collections.abc import Container, Iterator
from itertools import chain
from pathlib import Path

import more_itertools

from tag_space_tools.core.tag_finder import TagFinder
from tag_space_tools.core.tag_space_entry import Tag, TagSpaceEntry

logger = logging.getLogger(__name__)


def _dirGen(sortTag: list[Tag], tags: list[Tag], destDir: Path) -> Iterator[Path]:
    curPath = destDir
    for st in sortTag:
        if st in tags:
            curPath = curPath / st.title
            yield curPath


def sortFiles(
    sortTag: list[Tag],
    srcDir: Path | str,
    dstDir: Path | str,
    maxFilesInDir=20,
    *,
    recursive=True,
    excludeDir: Container[Path] = (),
    tagFinderDst: TagFinder | None = None,
    tagFinderSrc: TagFinder | None = None,
):
    """
    Move files and their tags from 'srcDir' to 'dstDir'.

    Subdirectory name is chosen based on moving file tags and 'sortTag' argument.

    :param sortTag: tag list defining order of sort
    :param srcDir: source directory
    :param dstDir: destination directory
    :param maxFilesInDir: If there are more than 'maxFilesInDir'
        then a new subdirectory will be created.
    :param recursive: If True then sorting is recursive.
    :param excludeDir: Directories that will be skipped when sorting.
    :param tagFinderDst: cached object for better performance
    :param tagFinderSrc: cached object for better performance
    """
    dstDirPath = Path(dstDir)
    dstDirPath.mkdir(exist_ok=True, parents=True)
    if tagFinderDst is None:
        tagFinderDst = TagFinder(dstDirPath)

    if tagFinderSrc is None:
        tagFinderSrc = TagFinder(srcDir)

    for tagEntry in tagFinderSrc.getTagEntryInDir(srcDir, recursive=recursive):

        lastDir = dstDirPath
        dirGen: Iterator[Path | None] = _dirGen(sortTag, tagEntry.tags, dstDirPath)
        windowed = more_itertools.windowed(chain(dirGen, (None,)), 2)

        for lastDir, nextDir in windowed:
            if nextDir and nextDir.exists():
                continue

            if lastDir is None:
                break

            if lastDir in excludeDir:
                continue

            taggedFilesCount = len(
                tagFinderDst.getTagEntryInDir(lastDir, recursive=False)
            )
            if taggedFilesCount < maxFilesInDir:
                tagEntry.move(lastDir)
                break

            if taggedFilesCount >= maxFilesInDir:
                tagEntry.move(lastDir)
                sortFiles(
                    sortTag,
                    lastDir,
                    dstDir,
                    maxFilesInDir,
                    recursive=False,
                    excludeDir=(lastDir,),
                    tagFinderDst=tagFinderDst,
                    tagFinderSrc=tagFinderSrc,
                )
                break

        else:
            _moveFile(tagEntry, lastDir)


def _moveFile(tagEntry: TagSpaceEntry, lastDir: Path | None):
    if lastDir is None:
        raise TypeError
    tagEntry.move(lastDir)

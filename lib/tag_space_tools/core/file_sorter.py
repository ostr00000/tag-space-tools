import logging
from itertools import chain
from pathlib import Path
from typing import Iterator, Union, Container

import more_itertools

from tag_space_tools.core.tag_finder import TagFinder
from tag_space_tools.core.tag_space_entry import Tag

logger = logging.getLogger(__name__)


def _dirGen(sortTag: list[Tag], tags: list[Tag], destDir: Path) -> Iterator[Path]:
    curPath = destDir
    for st in sortTag:
        if st in tags:
            curPath = curPath / st.title
            yield curPath


def sortFiles(sortTag: list[Tag],
              srcDir: Union[Path, str],
              destDir: Union[Path, str],
              maxFilesInDir=20,
              recursive=True,
              excludeDir: Container[Path] = (),
              tagFinderDest: TagFinder = None,
              tagFinderSrc: TagFinder = None):
    """
    Move files and their tags from 'srcDir' to 'destDir'.
    Subdirectory name is chosen based on moving file tags and 'sortTag' argument.

    :param sortTag: tag list defining order of sort
    :param srcDir: source directory
    :param destDir: destination directory
    :param maxFilesInDir: If there are more than 'maxFilesInDir'
        then a new subdirectory will be created.
    :param recursive: If True then sorting is recursive.
    :param excludeDir: Directories that will be skipped when sorting.
    :param tagFinderDest: cached object for better performance
    :param tagFinderSrc: cached object for better performance
    """
    destDir = Path(destDir)
    destDir.mkdir(exist_ok=True, parents=True)
    if tagFinderDest is None:
        tagFinderDest = TagFinder(destDir)

    if tagFinderSrc is None:
        tagFinderSrc = TagFinder(srcDir)

    for tagEntry in tagFinderSrc.getTagEntryInDir(srcDir, recursive=recursive):

        lastDir = destDir
        dirGen = _dirGen(sortTag, tagEntry.tags, destDir)
        for lastDir, nextDir in more_itertools.windowed(chain(dirGen, (None,)), 2):
            if nextDir and nextDir.exists():
                continue

            if lastDir is None:
                break

            if lastDir in excludeDir:
                continue

            taggedFilesCount = len(tagFinderDest.getTagEntryInDir(lastDir, recursive=False))
            if taggedFilesCount < maxFilesInDir:
                tagEntry.move(lastDir)
                break
            elif taggedFilesCount >= maxFilesInDir:
                tagEntry.move(lastDir)
                sortFiles(sortTag, lastDir, destDir, maxFilesInDir,
                          recursive=False, excludeDir=(lastDir,),
                          tagFinderDest=tagFinderDest, tagFinderSrc=tagFinderSrc)
                break

        else:
            tagEntry.move(lastDir)

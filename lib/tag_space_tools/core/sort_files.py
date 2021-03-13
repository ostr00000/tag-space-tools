import logging
import shutil
from pathlib import Path
from typing import Iterator, Union

from tag_space_tools.core.fix_tagspace import TagSpaceSearch
from tag_space_tools.core.tag_space_entry import Tag, TagSpaceEntry

logger = logging.getLogger(__name__)


def _dirGen(sortTag: list[Tag], tags: list[Tag], destDir: Path) -> Iterator[Path]:
    curPath = destDir
    for st in sortTag:
        if st in tags:
            curPath = curPath / st.title
            yield curPath


def _filesInFolderCount(folder: Path):
    return sum(1 for f in folder.glob('*') if f.is_file())


def _moveTagEntry(tagEntry: TagSpaceEntry, destDir: Path):
    metaDir = destDir / TagSpaceSearch.TAG_DIR
    metaDir.mkdir(exist_ok=True, parents=True)

    logger.debug(f"Moving {tagEntry.file} to {destDir / tagEntry.file.name}")
    shutil.move(tagEntry.file, destDir / tagEntry.file.name)
    shutil.move(tagEntry.configFile, metaDir / tagEntry.configFile.name)


def sortFiles(sortTag: list[Tag],
              srcDir: Union[Path, str],
              destDir: Union[Path, str],
              maxFilesInDir=20):
    """Move files and their tags from 'srcDir' to 'destDir'.
    If there are more than 'maxFilesInDir' then create subdirectory.
    Subdirectory name is chosen based on moving file tags and 'sortTag' argument.
    """
    destDir = Path(destDir)
    tagSpaceSearch = TagSpaceSearch(srcDir)
    for tagEntry in tagSpaceSearch.validTagEntries:

        lastDir = destDir
        for lastDir in _dirGen(sortTag, tagEntry.tags, destDir):
            if _filesInFolderCount(lastDir) <= maxFilesInDir:
                _moveTagEntry(tagEntry, lastDir)
                break
        else:
            _moveTagEntry(tagEntry, lastDir)

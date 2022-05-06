import logging
import os
import sys
import zlib
from collections import defaultdict
from pathlib import Path
from pprint import pprint
from typing import TypeVar, Callable, Iterable, Any

import progressbar

from tag_space_tools.core.tag_space_entry import TagSpaceEntry

try:
    from typing import TypeAlias
except ImportError:
    TypeAlias = object

logger = logging.getLogger(__name__)
T = TypeVar('T')


def getSize(path: Path):
    return path.stat().st_size


def getCrc(path: Path):
    with open(path, 'rb') as file:
        content = file.read(1024)
    checksum = zlib.crc32(content)
    return checksum


def genFilesRec(path: Path):
    for file in path.iterdir():
        if file.is_file():
            yield file
        elif file.is_dir() and file.name != TagSpaceEntry.TAG_DIR:
            yield from genFilesRec(file)


def progressBarIter(it: Iterable[T], totalSize: int) -> Iterable[T]:
    try:
        bar = progressbar.ProgressBar(
            maxval=totalSize,
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()],
        )
        bar.start()
    except IOError:  # no stdout/stderr
        yield from it
    else:
        for i, val in enumerate(it):
            yield val
            bar.update(i + 1)
        bar.finish()


NEW_KEY = TypeVar('NEW_KEY')
OLD_KEY = TypeVar('OLD_KEY')
VAL = TypeVar('VAL')


def nestedDictSize(dic: dict[T, list]):
    return sum(len(val) for val in dic.values())


def filterDuplicated(keyFun: Callable[[VAL], NEW_KEY],
                     dup: dict[OLD_KEY, list[VAL]]
                     ) -> dict[tuple[OLD_KEY, NEW_KEY], list[VAL]]:
    keyToValues = defaultdict(list)
    totalSize = nestedDictSize(dup)
    for oldKey, values in progressBarIter(dup.items(), totalSize=totalSize):
        for v in values:
            keyToValues[oldKey, keyFun(v)].append(v)

    return {k: val for k, val in keyToValues.items() if len(val) >= 2}


DUP_RESULT: TypeAlias = dict[Any, list[Path]]


def findDuplicates(path: os.PathLike | str,
                   filterFunctions: Iterable[Callable[[Path], T]] = (getSize, getCrc)
                   ) -> DUP_RESULT:
    path = Path(path)
    dup = {None: list(genFilesRec(path))}
    logger.debug(f'Filter stage 0: {nestedDictSize(dup)}')

    for stageNum, filterFun in enumerate(filterFunctions):
        dup = filterDuplicated(filterFun, dup)
        logger.debug(f'Filter stage {stageNum}: {nestedDictSize(dup)}')

    return dup


if __name__ == '__main__':
    pprint(findDuplicates(sys.argv[1]))

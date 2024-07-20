import logging
import sys
import zlib
from collections import defaultdict
from collections.abc import Callable, Iterable, Iterator
from pathlib import Path
from pprint import pformat
from typing import Any

import progressbar

from tag_space_tools.core.tag_space_entry import TagSpaceEntry

logger = logging.getLogger(__name__)


def getSize(path: Path) -> int:
    return path.stat().st_size


def getCrc(path: Path) -> int:
    with path.open('rb') as file:
        content = file.read(1024)
    return zlib.crc32(content)


def genFilesRec(path: Path) -> Iterable[Path]:
    for file in path.iterdir():
        if file.is_file():
            yield file
        elif file.is_dir() and file.name != TagSpaceEntry.TAG_DIR:
            yield from genFilesRec(file)


def progressBarIter[T](it: Iterable[T], totalSize: int) -> Iterable[T]:
    try:
        bar = progressbar.ProgressBar(
            maxval=totalSize,
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()],
        )
        bar.start()
    except OSError:  # no stdout/stderr
        yield from it
    else:
        for i, val in enumerate(it):
            yield val
            bar.update(i + 1)
        bar.finish()


def nestedDictSize(dic: dict[Any, list]) -> int:
    return sum(len(val) for val in dic.values())


type _LevelKey = tuple[int, ...]
type _LevelMap[P] = dict[_LevelKey, list[P]]


class DupAggregator[P]:
    def __init__(self, allObjects: list[P]):
        self.allObjects = allObjects
        logger.debug(f'Filter stage 0: {len(allObjects)}')

        level0: _LevelMap = {(0,): self.allObjects}
        self.levels: list[_LevelMap[P]] = [level0]

    def addLevel(self, keyFun: Callable[[P], int]):
        lastLevel = self.levels[-1]
        totalSize = nestedDictSize(lastLevel)
        keyToValues: _LevelMap[P] = defaultdict(list)

        for k, values in progressBarIter(lastLevel.items(), totalSize=totalSize):
            for v in values:
                keyToValues[*k, keyFun(v)].append(v)

        dupKeyToVal = {k: val for k, val in keyToValues.items() if len(val) > 1}
        self.levels.append(dupKeyToVal)
        logger.debug(f'Filter stage {self.levels}: {nestedDictSize(dupKeyToVal)}')

    def getAllLevels(self) -> Iterator[list[str]]:
        for level in self.levels:
            ret: list[str] = list(map(str, level.keys()))
            ret.extend(map(str, level.values()))
            yield ret


class PathDupAggregator(DupAggregator[Path]):
    def __init__(self, pathLike: str | Path):
        allObjects = list(genFilesRec(Path(pathLike)))
        super().__init__(allObjects)

        self.addLevel(getSize)
        self.addLevel(getCrc)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger.debug(pformat(PathDupAggregator(sys.argv[1]).levels))

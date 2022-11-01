import json
from pathlib import Path
from typing import Iterator

from pyqt_utils.python.json_serializable import deepMap
from tag_space_tools.core.tag_space_entry import Tag


def loadTagLibrary(path: str | Path) -> Iterator[Tag]:
    if not (path and Path(path).exists()):
        return []

    with open(path) as tagLibraryFile:
        tagLibrary = json.load(tagLibraryFile)

    return parseJson(tagLibrary)


def parseJson(tagJson) -> Iterator[Tag]:
    if 'tagGroups' in tagJson:
        yield from _parseTagLibraryJson(tagJson)
    else:
        yield from _parseTagToolsJson(tagJson)


def _parseTagLibraryJson(tagJson: dict) -> Iterator[Tag]:
    for group in tagJson['tagGroups']:
        for tag in group['children']:
            yield Tag.fromDict(tag)


def _parseTagToolsJson(tagJson: list) -> Iterator[Tag]:
    yield from deepMap(tagJson, (list, Tag.fromDict))

import json
from collections.abc import Iterator
from pathlib import Path

from tag_space_tools.core.tag_space_entry import Tag


def loadTagLibrary(path: str | Path) -> Iterator[Tag]:
    if not path:
        return []

    if not (libPath := Path(path)).exists():
        return []

    with libPath.open() as tagLibraryFile:
        tagLibrary = json.load(tagLibraryFile)

    if isinstance(tagLibrary, dict) and 'tagGroups' in tagLibrary:
        yield from _parseTagLibraryJson(tagLibrary)
    else:
        yield from [Tag.fromDict(t) for t in tagLibrary]


def _parseTagLibraryJson(tagJson: dict) -> Iterator[Tag]:
    for group in tagJson['tagGroups']:
        for tag in group['children']:
            yield Tag.fromDict(tag)

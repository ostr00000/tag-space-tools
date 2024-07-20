import inspect
import itertools
import json
import logging
import shutil
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import datetime
from functools import cached_property
from pathlib import Path
from typing import Literal, TypedDict, overload

logger = logging.getLogger(__name__)


@dataclass
class Tag:
    title: str
    type: str = ''
    color: str = ''
    textcolor: str = ''

    @classmethod
    def fromDict(cls, env):
        param = inspect.signature(cls).parameters
        return cls(**{k: v for k, v in env.items() if k in param})

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.title

        if not isinstance(other, Tag):
            return NotImplemented

        return self.title == other.title

    def __hash__(self):
        return hash(self.title)


class TagsSerializer(list[Tag]):
    """Class used for serialization and deserialization of `Tag` class."""

    @classmethod
    def deserialize(cls, tagText: str) -> list[Tag]:
        tags = json.loads(tagText)
        return [Tag.fromDict(t) for t in tags]

    @classmethod
    def serialize(cls, sortedTags: list[Tag]) -> str:
        return json.dumps([asdict(t) for t in sortedTags])


class TagDict(TypedDict):
    type: str
    title: str
    description: str
    functionality: str
    style: str
    icon: str
    color: str
    textcolor: str
    created_date: str
    modified_date: str


class ConfigDict[TagType: (TagDict, Tag)](TypedDict):
    # `tags` value may be a python wrapper or raw dict
    tags: dict[str, TagType]
    description: str
    color: str
    appVersionCreated: str
    appName: str
    appVersionUpdated: str
    lastUpdated: str


@dataclass
class TagSpaceEntry:
    TAG_DIR = '.ts'
    TSM_FILE = 'tsm.json'
    TAG_SUFFIX = '.json'

    file: Path | None = None
    configFile: Path | None = None

    def __post_init__(self):
        if self.configFile is not None and not self.configFile.exists():
            self.configFile = None

    @property
    def requireFile(self) -> Path:
        if self.file is None:
            msg = f"No file for {self}"
            raise ValueError(msg)
        return self.file

    @property
    def requireConfigFile(self) -> Path:
        if self.configFile is None:
            msg = f"No config file for {self}"
            raise ValueError(msg)
        return self.configFile

    def isValid(self):
        return self.file is not None and self.configFile is not None

    @cached_property
    def tags(self) -> list[Tag]:
        with self._configContext() as configJson:
            return list(configJson['tags'].values())

    def renameTag(self, fromTagName: str, toTagName: str):
        """If file has *fromTagName* then change this tag to *toTagName*."""
        if fromTagName not in self.tags:
            return False

        with self._configContext(edit=True) as configJson:
            changingTag = configJson['tags'].get(fromTagName, {})
            logger.info(
                f"Rename tag:'{changingTag['title']}' to '{toTagName}' "
                f"for file '{self.requireFile.name}'"
            )
            changingTag['title'] = toTagName
            changingTag['modified_date'] = datetime.now().astimezone().isoformat()

        for t in self.tags:
            if t.title == fromTagName:
                t.title = toTagName
                break

        return True

    def removeTag(self, removeTagName: str):
        if removeTagName not in self.tags:
            return False

        with self._configContext(edit=True) as configJson:
            removingTag: dict = configJson['tags'].get(removeTagName, {})
            removingTag.pop('title', None)

        for t in self.tags:
            if t.title == removeTagName:
                self.tags.remove(t)
                break
        return True

    def addTag(self, tag: Tag):
        if tag.title in self.tags:
            return True

        with self._configContext(edit=True) as configJson:
            addingTag: dict = configJson['tags']
            addingTag[tag.title] = asdict(tag)
            addingTag['modified_date'] = datetime.now().astimezone().isoformat()

        self.tags.append(tag)
        return True

    @overload
    @contextmanager
    def _configContext(
        self, *, edit: Literal[True]
    ) -> Iterator[ConfigDict[TagDict]]: ...

    @overload
    @contextmanager
    def _configContext(
        self, *, edit: Literal[False] = False
    ) -> Iterator[ConfigDict[Tag]]: ...

    @contextmanager
    def _configContext(self, *, edit=False) -> Iterator[ConfigDict]:
        mode = 'r+' if edit else 'r'
        with self.requireConfigFile.open(mode, encoding='utf-8-sig') as cf:
            configJson = json.load(cf)
            try:
                tags = {
                    tagJson['title']: tagJson if edit else Tag.fromDict(tagJson)
                    for tagJson in configJson['tags']
                }
            except KeyError:
                tags = {}
            configJson['tags'] = tags

            yield configJson
            if edit:
                configJson['tags'] = list(configJson['tags'].values())
                configJson['lastUpdated'] = datetime.now().astimezone().isoformat()
                cf.seek(0)
                json.dump(configJson, cf)
                cf.truncate()

    def move(self, destDir: Path):
        """Move file with its meta file to *destDir*."""
        if self.file is not None:
            destDir.mkdir(exist_ok=True, parents=True)
            destFilePath = generateUniqueFile(destDir / self.requireFile.name)

            logger.debug(f"Moving {self.requireFile} to {destFilePath}")
            shutil.move(self.requireFile, destFilePath)
            self.file = destFilePath

        if self.configFile is not None:
            metaDir = destDir / self.TAG_DIR
            metaDir.mkdir(exist_ok=True, parents=True)

            if self.file is not None:
                fileName = self.requireFile.name + self.TAG_SUFFIX
            else:
                fileName = self.requireConfigFile.name
            configDestFile = metaDir / fileName

            logger.debug(f"Moving {self.requireConfigFile} to {configDestFile}")
            shutil.move(self.requireConfigFile, configDestFile)
            self.configFile = configDestFile


def generateUniqueFile(file: Path) -> Path:
    baseStem = file.stem
    for i in itertools.count(start=1):
        if not file.exists():
            return file
        file = file.with_stem(f'{baseStem}_{i}')

    raise ValueError

import inspect
import json
import logging
import shutil
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from datetime import datetime
from functools import cached_property
from pathlib import Path
from typing import Optional, List, ClassVar, TypedDict, Dict, ContextManager, TypeVar

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
        tag = cls(**{
            k: v for k, v in env.items()
            if k in param})
        return tag

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.title

        if not isinstance(other, Tag):
            raise NotImplemented

        return self.title == other.title

    def __hash__(self):
        return hash(self.title)


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


TagType = TypeVar('TagType', TagDict, Tag)


class ConfigDict(TypedDict):
    tags: Dict[str, TagType]
    description: str
    color: str
    appVersionCreated: str
    appName: str
    appVersionUpdated: str
    lastUpdated: str


@dataclass
class TagSpaceEntry:
    TAG_DIR: ClassVar = '.ts'
    TSM_FILE: ClassVar = 'tsm.json'

    file: Optional[Path] = None
    configFile: Optional[Path] = None

    def __post_init__(self):
        if not self.configFile.exists():
            self.configFile = None

    def isValid(self):
        return (self.file is not None
                and self.configFile is not None)

    @cached_property
    def tags(self) -> List[Tag]:
        with self._configContext() as configJson:
            return list(configJson['tags'].values())

    def renameTag(self, fromTagName: str, toTagName: str):
        """If file has *fromTagName* then change this tag to *toTagName*."""
        if fromTagName not in self.tags:
            return False

        with self._configContext(edit=True) as configJson:
            changingTag = configJson['tags'].get(fromTagName, {})
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

    @contextmanager
    def _configContext(self, edit=False) -> ContextManager[ConfigDict]:
        mode = 'r+' if edit else 'r'
        with open(self.configFile, mode, encoding='utf-8-sig') as cf:
            configJson = json.load(cf)
            try:
                tags = {tagJson['title']: tagJson if edit else Tag.fromDict(tagJson)
                        for tagJson in configJson['tags']}
            except KeyError:
                tags = []
            configJson['tags'] = tags

            yield configJson
            if edit:
                configJson['tags'] = [t for t in configJson['tags'].values()]
                configJson['lastUpdated'] = datetime.now().astimezone().isoformat()
                cf.seek(0)
                json.dump(configJson, cf)
                cf.truncate()

    def move(self, destDir: Path):
        """Move file with its meta file to *destDir*."""
        metaDir = destDir / self.TAG_DIR
        metaDir.mkdir(exist_ok=True, parents=True)

        destFile = destDir / self.file.name
        logger.debug(f"Moving {self.file} to {destFile}")
        shutil.move(self.file, destFile)
        self.file = destFile

        destFile = metaDir / self.configFile.name
        shutil.move(self.configFile, destFile)
        self.configFile = destFile

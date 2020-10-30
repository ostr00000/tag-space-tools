import inspect
import json
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Optional, List


@dataclass
class Tag:
    title: str
    type: str
    color: str
    textcolor: str

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


@dataclass
class TagSpaceEntry:
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
        with open(self.configFile, encoding='utf-8-sig') as cf:
            configJson = json.load(cf)

        try:
            tags = [Tag.fromDict(tagJson) for tagJson in configJson['tags']]
            return tags
        except KeyError:
            return []

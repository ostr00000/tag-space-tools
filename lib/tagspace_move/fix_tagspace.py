import logging
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from tagspace_move.tag_space_entry import TagSpaceEntry

logger = logging.getLogger(__name__)


class TagSpaceSearch:
    """Files - normal files on disk,
    Config files - special files from tagspace located in TAG_DIR.
    """

    TAG_DIR = '.ts'
    TSM_FILE = 'tsm.json'

    def __init__(self, location: Path, recursive=True):
        self.location = location
        self.recursive = recursive

        self.missingTagFiles: Dict[str, List[TagSpaceEntry]] = defaultdict(list)
        self.missingTagConfigs: Dict[str, List[TagSpaceEntry]] = defaultdict(list)
        self._findTagSpace(self.location)
        self.missingTagFiles = dict(self.missingTagFiles)
        self.missingTagConfigs = dict(self.missingTagConfigs)

    def match(self):
        """Match config file to file base on name and move to file location"""
        for missingTagFileName, missingTagFiles in self.missingTagFiles.items():
            if len(missingTagFiles) > 1:
                logger.warning(f"Too many files for '{missingTagFileName}'")
                continue

            missingTagFile = missingTagFiles[0]

            if configs := self.missingTagConfigs.get(missingTagFileName):
                if len(configs) == 1:
                    configTag = configs[0].configFile
                    targetPath = missingTagFile.file.parent / self.TAG_DIR / configTag.name

                    if targetPath.exists():
                        logger.error(f'File already exists {targetPath}')
                    else:
                        logger.info(f"Matched file config '{configTag.name}' to '{targetPath}'")
                        logger.debug("Moving")
                        targetPath.parent.mkdir(exist_ok=True, parents=True)
                        shutil.move(configTag, targetPath)
                        logger.debug("Moved")

                else:
                    files = '\n'.join(str(c.configFile) for c in configs)
                    logger.warning(f"There are more than one matching file: [\n{files}\n]")
            else:
                logger.error(f"Cannot find config for file '{missingTagFileName}'")

    def _findTagSpace(self, location: Path):
        """Find all files and config that do not have corresponding files"""
        tagDir = location / self.TAG_DIR
        metaFiles = set(self._findMetaFiles(tagDir))

        for file in location.iterdir():
            if file.is_dir():
                if file.name == self.TAG_DIR:
                    continue
                elif self.recursive:
                    self._findTagSpace(file)

            elif file.is_file():
                tse = TagSpaceEntry(file, tagDir / (file.name + '.json'))
                try:
                    metaFiles.remove(tse.configFile)
                except KeyError:
                    pass
                self._addEntry(tse)

        for metaFile in metaFiles:
            self._addEntry(TagSpaceEntry(configFile=metaFile))

    def _addEntry(self, tse: TagSpaceEntry):
        """Add an entry to missing list if the entry is invalid"""
        if tse.isValid():
            return

        if tse.file is None and tse.configFile is not None:
            name = tse.configFile.name.removesuffix('.json')
            self.missingTagConfigs[name].append(tse)

        elif tse.file is not None and tse.configFile is None:
            self.missingTagFiles[tse.file.name].append(tse)

    def _findMetaFiles(self, folder: Path):
        """Find config for files in 'folder'."""
        if not folder.exists():
            return

        for file in folder.iterdir():
            if file.suffix.endswith('json'):
                if file.name != self.TSM_FILE:
                    yield file



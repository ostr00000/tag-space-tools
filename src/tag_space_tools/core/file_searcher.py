import contextlib
import logging
import shutil
from collections import defaultdict
from pathlib import Path

from pyqt_utils.python.typing_const import StrPath

from tag_space_tools.core.tag_space_entry import TagSpaceEntry

logger = logging.getLogger(__name__)


class TagSpaceSearcher:
    """Class for searching tags.

    Files - normal files on disk,
    Config files - special files from Tag Spaces located in TagSpaceEntry.TAG_DIR.
    """

    def __init__(self, location: StrPath, *, recursive=True):
        self.location = Path(location)
        self.recursive = recursive

        self.missingTagFiles: dict[str, list[TagSpaceEntry]] = defaultdict(list)
        self.missingTagConfigs: dict[str, list[TagSpaceEntry]] = defaultdict(list)
        self.validTagEntries: list[TagSpaceEntry] = []

        self._findTagSpace(self.location)
        self.missingTagFiles = dict(self.missingTagFiles)
        self.missingTagConfigs = dict(self.missingTagConfigs)

    def match(self):
        """Match config file to file base on name and move to file location."""
        for missingTagFileName, missingTagFiles in self.missingTagFiles.items():
            match missingTagFiles:
                case [mtf] if mtf.file is not None:
                    mtfFile = mtf.file
                case [mtf]:
                    logger.warning(f"Missing file in {mtf}")
                    continue
                case _:
                    logger.warning(f"Too many files for '{missingTagFileName}'")
                    continue

            match (configs := self.missingTagConfigs.get(missingTagFileName, [])):
                case [conf] if conf.configFile is not None:
                    configTag = conf.requireConfigFile
                case [conf]:
                    logger.warning(f"Missing configuration file {conf}")
                    continue
                case []:
                    msg = f"Cannot find config for file '{missingTagFileName}'"
                    logger.warning(msg)
                    continue
                case _:
                    files = '\n'.join(str(c.configFile) for c in configs)
                    msg = f"There are more than one matching file: [\n{files}\n]"
                    logger.error(msg)
                    continue

            targetPath = mtfFile.parent / TagSpaceEntry.TAG_DIR / configTag.name
            if targetPath.exists():
                logger.error(f'File already exists {targetPath}')
                continue

            logger.info(f"Matched file config '{configTag.name}' to '{targetPath}'")
            logger.debug("Moving")
            targetPath.parent.mkdir(exist_ok=True, parents=True)
            shutil.move(configTag, targetPath)
            logger.debug("Moved")

    def _findTagSpace(self, location: Path):
        """Find all files and config that do not have corresponding files."""
        try:
            if not location.exists():
                return
        except OSError:
            logger.exception(f"Cannot check {location}")
            return

        tagDir = location / TagSpaceEntry.TAG_DIR
        metaFiles = set(self._findMetaFiles(tagDir))

        for file in location.iterdir():
            if file.is_dir():
                if file.name == TagSpaceEntry.TAG_DIR:
                    continue
                if self.recursive:
                    self._findTagSpace(file)

            elif file.is_file():
                tse = TagSpaceEntry(file, tagDir / (file.name + '.json'))
                if tse.configFile:
                    with contextlib.suppress(KeyError):
                        metaFiles.remove(tse.requireConfigFile)
                self._addEntry(tse)

        for metaFile in metaFiles:
            self._addEntry(TagSpaceEntry(configFile=metaFile))

    def _addEntry(self, tse: TagSpaceEntry):
        """Add an entry to missing list if the entry is invalid."""
        if tse.isValid():
            self.validTagEntries.append(tse)
            return

        if tse.file is None and tse.configFile is not None:
            name = tse.requireConfigFile.name.removesuffix('.json')
            self.missingTagConfigs[name].append(tse)

        elif tse.file is not None and tse.configFile is None:
            self.missingTagFiles[tse.requireFile.name].append(tse)

    @staticmethod
    def _findMetaFiles(folder: Path):
        """Find config for files in 'folder'."""
        if not folder.exists():
            return

        for file in folder.iterdir():
            if not file.suffix.endswith('json'):
                continue

            if file.name == TagSpaceEntry.TSM_FILE:
                continue

            yield file

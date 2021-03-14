import json
import logging
from pathlib import Path
from typing import Iterator, Iterable

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QWidget

from pyqt_utils.metaclass.slot_decorator import SlotDecoratorMeta
from pyqt_utils.python.json_serializable import deepMap
from pyqt_utils.ui_base_widget import BaseWidget
from tag_space_tools.core.sort_files import sortFiles
from tag_space_tools.core.tag_space_entry import Tag
from tag_space_tools.gui.settings import settings
from tag_space_tools.ui.ui_tag_sorter import Ui_TagSorter

logger = logging.getLogger(__name__)


class TagItem(QListWidgetItem):
    def __init__(self, tag: Tag, parent=None):
        super().__init__(tag.title, parent=parent)
        self.tag = tag
        self.setBackground(self._convertColor(tag.color))
        self.setForeground(self._convertColor(tag.textcolor))

    @staticmethod
    def _convertColor(color: str) -> QColor:
        if color.startswith('#'):
            colorRgb = color[:7]
            return QColor(colorRgb)
        else:
            return QColor(color)


class TagSorter(Ui_TagSorter, BaseWidget, QWidget, metaclass=SlotDecoratorMeta):
    def __post_init__(self, *args, **kwargs):
        super(TagSorter, self).__post_init__(*args, **kwargs)
        self.loadTagsButton.clicked.connect(self.onLoadTagsButton)
        self.fromButton.clicked.connect(self.onFromButtonClicked)
        self.toButton.clicked.connect(self.onToButtonClicked)
        self.maxFilesPerLevelSpinBox.valueChanged.connect(self.onMaxFilesChanged)
        self.removeTagButton.clicked.connect(self.onRemoveTagClicked)
        self.moveFilesButton.clicked.connect(self.onMoveFilesClicked)
        self.saveButton.clicked.connect(self.onSaveButtonClicked)

        self.maxFilesPerLevelSpinBox.setValue(settings.MAX_FILES_PER_LEVEL)
        self.toLineEdit.setText(settings.TO_PATH)
        self.fromLineEdit.setText(settings.FROM_PATH)

        settings.SORTED_TAGS = []
        if sortedTags := settings.SORTED_TAGS:
            self._loadTags(sortedTags)

    def _loadTags(self, sortedTags: Iterable[Tag]):
        self.listWidget.clear()
        for tag in sortedTags:
            self.listWidget.addItem(TagItem(tag))

    def onLoadTagsButton(self):
        path, ext = QFileDialog.getOpenFileName(
            self, "Select tag library", filter='*.json')
        if not path:
            return
        settings.LIBRARY_PATH = path
        self._loadTagLibrary(path)
        self._saveSortedTags()

    def _loadTagLibrary(self, path: str):
        if not (path and Path(path).exists()):
            return

        with open(path, 'r') as tagLibraryFile:
            tagLibrary = json.load(tagLibraryFile)

        self._loadTags(self._parseJson(tagLibrary))

    def _parseJson(self, tagJson) -> Iterator[Tag]:
        if 'tagGroups' in tagJson:
            yield from self._parseTagLibraryJson(tagJson)
        else:
            yield from self._parseTagToolsJson(tagJson)

    @staticmethod
    def _parseTagLibraryJson(tagJson: dict) -> Iterator[Tag]:
        for group in tagJson['tagGroups']:
            for tag in group['children']:
                yield Tag.fromDict(tag)

    @staticmethod
    def _parseTagToolsJson(tagJson: list) -> Iterator[Tag]:
        yield from deepMap(tagJson, (list, Tag.fromDict))

    def onRemoveTagClicked(self):
        for item in reversed(self.listWidget.selectedItems()):
            row = self.listWidget.row(item)
            self.listWidget.takeItem(row)
        self._saveSortedTags()

    def _saveSortedTags(self):
        settings.SORTED_TAGS = self.getSortTags()

    def getSortTags(self) -> list[Tag]:
        sortTags = []
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            sortTags.append(getattr(item, 'tag'))
        return sortTags

    def onFromButtonClicked(self):
        path = QFileDialog.getExistingDirectory(
            self, "Select folder with unsorted files")
        if not path:
            return
        settings.FROM_PATH = path
        self.fromLineEdit.setText(path)

    def onToButtonClicked(self):
        path = QFileDialog.getExistingDirectory(
            self, "Select main library folder")
        if not path:
            return
        settings.TO_PATH = path
        self.toLineEdit.setText(path)

    def onMaxFilesChanged(self):
        val = self.maxFilesPerLevelSpinBox.value()
        settings.MAX_FILES_PER_LEVEL = val

    def onMoveFilesClicked(self):
        sortTags = self.getSortTags()
        if not sortTags:
            return

        fromPath = self.fromLineEdit.text()
        if not (fromPath and Path(fromPath).exists()):
            return

        toPath = self.toLineEdit.text()
        if not (toPath and Path(toPath).exists()):
            return

        maxFiles = self.maxFilesPerLevelSpinBox.value()
        sortFiles(sortTags, fromPath, toPath, maxFiles)

    def onSaveButtonClicked(self):
        savePath: str
        savePath, ext = QFileDialog.getSaveFileName(
            parent=self, caption="Select save location",
            directory=settings.LAST_SAVE_FILE, filter='*.json')
        if not savePath:
            return

        if not savePath.endswith('.json'):
            savePath += '.json'

        settings.LAST_SAVE_FILE = savePath
        Path(savePath).parent.mkdir(parents=True, exist_ok=True)

        with open(savePath, 'w') as saveFile:
            saveFile.write(json.dumps(self.getSortTags(), default=lambda x: x.__dict__))

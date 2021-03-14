import logging
from pathlib import Path

from PyQt5.QtWidgets import QWidget, QFileDialog

from pyqt_utils.metaclass.slot_decorator import SlotDecoratorMeta
from pyqt_utils.ui_base_widget import BaseWidget
from tag_space_tools.core.sort_files import sortFiles
from tag_space_tools.gui.settings import settings
from tag_space_tools.gui.tag_sorter.parser import loadTagLibrary
from tag_space_tools.ui.ui_tag_sorter import Ui_TagSorter

logger = logging.getLogger(__name__)


class TagSorter(Ui_TagSorter, BaseWidget, QWidget, metaclass=SlotDecoratorMeta):
    def __post_init__(self, *args, **kwargs):
        super(TagSorter, self).__post_init__(*args, **kwargs)
        self.loadTagsButton.clicked.connect(self.onLoadTagsButton)
        self.fromButton.clicked.connect(self.onFromButtonClicked)
        self.toButton.clicked.connect(self.onToButtonClicked)
        self.maxFilesPerLevelSpinBox.valueChanged.connect(self.onMaxFilesChanged)
        self.removeTagButton.clicked.connect(self.listWidget.removeSelected)
        self.moveFilesButton.clicked.connect(self.onMoveFilesClicked)
        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.listWidget.dataChanged.connect(self.onDataChanged)

        self.maxFilesPerLevelSpinBox.setValue(settings.MAX_FILES_PER_LEVEL)
        self.toLineEdit.setText(settings.TO_PATH)
        self.fromLineEdit.setText(settings.FROM_PATH)

        if sortedTags := settings.SORTED_TAGS:
            self.listWidget.addItems(sortedTags)

    def onDataChanged(self):
        self._saveSortedTags()

    def _saveSortedTags(self):
        settings.SORTED_TAGS = self.listWidget.getSortTags()

    def onLoadTagsButton(self):
        path, ext = QFileDialog.getOpenFileName(
            self, "Select tag library", filter='*.json')
        if not path:
            return
        settings.LIBRARY_PATH = path
        self.listWidget.replaceTags(loadTagLibrary(path))

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
        sortTags = self.listWidget.getSortTags()
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
        self.listWidget.saveToFile(savePath)

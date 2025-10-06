import logging
import os
from pathlib import Path

from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QWidget
from pyqt_utils.metaclass.slot_decorator import SlotDecoratorMeta
from pyqt_utils.python.decorators import cursorDecFactory
from pyqt_utils.widgets.base_ui_widget import BaseUiWidget

from tag_space_tools.core.file_sorter import sortFiles
from tag_space_tools.gui.settings import TagSpacePluginSettings, tsSettings
from tag_space_tools.gui.tag_sorter.parser import loadTagLibrary
from tag_space_tools.ui.tag_sorter_ui import Ui_TagSorter

logger = logging.getLogger(__name__)


class TagSorter(Ui_TagSorter, BaseUiWidget, QWidget, metaclass=SlotDecoratorMeta):
    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)

        self.toPath = TagSpacePluginSettings.LIBRARY_PATH.createWidgetWithLabel(
            tsSettings, self, layoutType=QVBoxLayout
        )
        self.toPath.replaceWidget(self.toFolderPlaceholder)

        self.fromPath = TagSpacePluginSettings.UNSORTED_PATH.createWidgetWithLabel(
            tsSettings, self, layoutType=QVBoxLayout
        )
        self.fromPath.replaceWidget(self.fromFolderPlaceholder)

        self.maxFiles = (
            TagSpacePluginSettings.MAX_FILES_PER_LEVEL.createWidgetWithLabel(
                tsSettings, self, layoutType=QVBoxLayout
            )
        )
        self.maxFiles.replaceWidget(self.maxFilesPlaceholder)

        self.loadTagsButton.clicked.connect(self.onLoadTagsButton)
        self.removeTagButton.clicked.connect(self.listWidget.removeSelected)
        self.listWidget.dataChangedSig.connect(self.onDataChanged)
        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.moveFilesButton.clicked.connect(self.onMoveFilesClicked)
        self.emptyFolderCleanButton.clicked.connect(self.onCleanEmptyFolders)

        if sortedTags := tsSettings.SORTED_TAGS:
            self.listWidget.addItems(sortedTags)

    def onDataChanged(self):
        self._saveSortedTags()

    def _saveSortedTags(self):
        tsSettings.SORTED_TAGS = self.listWidget.getAllTags()

    @cursorDecFactory()
    def onLoadTagsButton(self):
        path, _ext = QFileDialog.getOpenFileName(
            self,
            "Select tag library",
            directory=tsSettings.LAST_SAVE_FILE,
            filter='*.json',
        )
        if not path:
            return
        tsSettings.SORT_FILE_LIBRARY = path
        self.listWidget.updateTags(loadTagLibrary(path))

    @cursorDecFactory()
    def onSaveButtonClicked(self):
        savePath, _ext = QFileDialog.getSaveFileName(
            parent=self,
            caption="Select save location",
            directory=tsSettings.LAST_SAVE_FILE,
            filter='*.json',
        )
        if not savePath:
            return

        if not savePath.endswith('.json'):
            savePath += '.json'

        tsSettings.LAST_SAVE_FILE = savePath
        self.listWidget.saveToFile(savePath)

    @staticmethod
    @cursorDecFactory()
    def onMoveFilesClicked():
        fromPath = tsSettings.UNSORTED_PATH
        toPath = tsSettings.LIBRARY_PATH
        sortTags = tsSettings.SORTED_TAGS
        maxFiles = tsSettings.MAX_FILES_PER_LEVEL
        sortFiles(sortTags, fromPath, toPath, maxFiles)

    @staticmethod
    @cursorDecFactory()
    def onCleanEmptyFolders():
        libPath = tsSettings.LIBRARY_PATH
        changed = True
        while changed:
            changed = False

            for dirPath, dirNames, fileNames in os.walk(libPath):
                if dirNames or fileNames:
                    continue

                logger.info(f"Removing {dirPath}")
                try:
                    Path(dirPath).rmdir()
                    changed = True
                except OSError:
                    logger.exception(f"Cannot remove {dirPath}")

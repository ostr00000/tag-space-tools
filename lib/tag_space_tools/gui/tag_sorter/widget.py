import logging
import os

from PyQt5.QtWidgets import QWidget, QFileDialog, QVBoxLayout

from pyqt_utils.metaclass.slot_decorator import SlotDecoratorMeta
from pyqt_utils.widgets.base_widget import BaseWidget
from tag_space_tools.core.file_sorter import sortFiles
from tag_space_tools.gui.settings import settings, TagSpacePluginSettings
from tag_space_tools.gui.tag_sorter.parser import loadTagLibrary
from tag_space_tools.ui.ui_tag_sorter import Ui_TagSorter

logger = logging.getLogger(__name__)


class TagSorter(Ui_TagSorter, BaseWidget, QWidget, metaclass=SlotDecoratorMeta):
    def __post_init__(self, *args, **kwargs):
        super(TagSorter, self).__post_init__(*args, **kwargs)

        self.toPath = TagSpacePluginSettings.LIBRARY_PATH.createWidgetWithLabel(
            settings, self, layoutType=QVBoxLayout)
        self.toPath.replaceWidget(self.toFolderPlaceholder)

        self.fromPath = TagSpacePluginSettings.UNSORTED_PATH.createWidgetWithLabel(
            settings, self, layoutType=QVBoxLayout)
        self.fromPath.replaceWidget(self.fromFolderPlaceholder)

        self.maxFiles = TagSpacePluginSettings.MAX_FILES_PER_LEVEL. \
            createWidgetWithLabel(settings, self, layoutType=QVBoxLayout)
        self.maxFiles.replaceWidget(self.maxFilesPlaceholder)

        self.loadTagsButton.clicked.connect(self.onLoadTagsButton)
        self.removeTagButton.clicked.connect(self.listWidget.removeSelected)
        self.listWidget.dataChanged.connect(self.onDataChanged)
        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.moveFilesButton.clicked.connect(self.onMoveFilesClicked)
        self.emptyFolderCleanButton.clicked.connect(self.onCleanEmptyFolders)

        if sortedTags := settings.SORTED_TAGS:
            self.listWidget.addItems(sortedTags)

    def onDataChanged(self):
        self._saveSortedTags()

    def _saveSortedTags(self):
        settings.SORTED_TAGS = self.listWidget.getAllTags()

    def onLoadTagsButton(self):
        path, ext = QFileDialog.getOpenFileName(
            self, "Select tag library",
            directory=settings.LAST_SAVE_FILE, filter='*.json')
        if not path:
            return
        settings.SORT_FILE_LIBRARY = path
        self.listWidget.updateTags(loadTagLibrary(path))

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

    @staticmethod
    def onMoveFilesClicked():
        fromPath = settings.UNSORTED_PATH
        toPath = settings.LIBRARY_PATH
        sortTags = settings.SORTED_TAGS
        maxFiles = settings.MAX_FILES_PER_LEVEL
        sortFiles(sortTags, fromPath, toPath, maxFiles)

    @staticmethod
    def onCleanEmptyFolders():
        libPath = settings.LIBRARY_PATH
        for dirPath, dirNames, fileNames in os.walk(libPath):
            if not dirNames and not fileNames:
                logger.info(f"Removing {dirPath}")
                try:
                    os.rmdir(dirPath)
                except OSError:
                    logger.exception(f"Cannot remove {dirPath}")

import logging

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
        self.toPath.button.clicked.connect(self.onToButtonClicked)
        self.layout().replaceWidget(self.toFolderPlaceholder, self.toPath)
        self.toFolderPlaceholder.deleteLater()

        self.fromPath = TagSpacePluginSettings.UNSORTED_PATH.createWidgetWithLabel(
            settings, self, layoutType=QVBoxLayout)
        self.fromPath.button.clicked.connect(self.onFromButtonClicked)
        self.layout().replaceWidget(self.fromFolderPlaceholder, self.fromPath)
        self.fromFolderPlaceholder.deleteLater()

        self.maxFiles = TagSpacePluginSettings.MAX_FILES_PER_LEVEL. \
            createWidgetWithLabel(settings, self, layoutType=QVBoxLayout)
        self.maxFiles.button.clicked.connect(self.onMaxFilesChanged)
        self.layout().replaceWidget(self.maxFilesPlaceholder, self.maxFiles)
        self.maxFilesPlaceholder.deleteLater()

        self.loadTagsButton.clicked.connect(self.onLoadTagsButton)
        self.removeTagButton.clicked.connect(self.listWidget.removeSelected)
        self.listWidget.dataChanged.connect(self.onDataChanged)
        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.moveFilesButton.clicked.connect(self.onMoveFilesClicked)

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
        settings.SORT_FILE_LIBRARY = path
        self.listWidget.replaceTags(loadTagLibrary(path))

    def onFromButtonClicked(self):
        settings.UNSORTED_PATH = self.fromPath.getValue()

    def onToButtonClicked(self):
        settings.LIBRARY_PATH = self.toPath.getValue()

    def onMaxFilesChanged(self):
        settings.MAX_FILES_PER_LEVEL = self.maxFiles.getValue()

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

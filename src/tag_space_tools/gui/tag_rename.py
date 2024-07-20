from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QWidget
from pyqt_utils.widgets.base_ui_widget import BaseUiWidget

from tag_space_tools.core import tagSpaceCoreName
from tag_space_tools.core.tag_finder import TagFinder
from tag_space_tools.gui.settings import TagSpacePluginSettings, tsSettings
from tag_space_tools.gui.tag_fixer.text_handler import TextEditHandler
from tag_space_tools.ui.tag_rename_ui import Ui_TagRename

if TYPE_CHECKING:
    from pyqt_settings.field.base import Field


class TagRename(Ui_TagRename, BaseUiWidget, QWidget):
    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self.textHandler = TextEditHandler(
            self.textEdit, self.treeView, self.filterLineEdit
        )

        field: Field = TagSpacePluginSettings.LIBRARY_PATH
        self.libraryWidget = field.createWidgetWithLabel(tsSettings)
        self.libraryWidget.replaceWidget(self.libraryPlaceholder)

        TagSpacePluginSettings.LIBRARY_PATH.valueChanged.connect(self.onReset)
        self.toComboBox.currentTextChanged.connect(self.onToComboBoxTextChanged)
        self.renameButton.clicked.connect(self.onRenameButtonClicked)
        self.refreshButton.clicked.connect(self.onReset)

        self.onReset()

    def onReset(self):
        tags = TagFinder(tsSettings.LIBRARY_PATH).findAllTags()
        self.fromComboBox.clear()
        self.fromComboBox.addItems(tags)
        self.toComboBox.clear()
        self.toComboBox.addItems(tags)

    def onToComboBoxTextChanged(self, changedText: str):
        self.toLineEdit.setText(changedText)

    def onRenameButtonClicked(self):
        if not (fromTag := self.fromComboBox.currentText()):
            return

        if not (toTag := self.toLineEdit.text()):
            return

        with self.textHandler.useForLogger(tagSpaceCoreName):
            tagFinder = TagFinder(tsSettings.LIBRARY_PATH)
            for tagEntry in tagFinder.genEntriesWithTag(fromTag):
                tagEntry.renameTag(fromTag, toTag)

        self.onReset()

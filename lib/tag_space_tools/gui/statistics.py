from enum import Enum

from PyQt5.QtGui import QShowEvent
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from pyqt_settings.field.base import Field
from pyqt_utils.widgets.base_widget import BaseWidget
from tag_space_tools.core.tag_finder import TagFinder
from tag_space_tools.gui.settings import TagSpacePluginSettings, settings
from tag_space_tools.ui.statistic_widget_ui import Ui_StatisticWidget


class TagStatistics(Ui_StatisticWidget, BaseWidget, QWidget):
    class TableColumn(Enum):
        TAG_NAME = 0
        COUNT = 1
        FILES = 2

    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)

        field: Field = TagSpacePluginSettings.LIBRARY_PATH
        self.libraryWidget = field.createWidgetWithLabel(settings)
        self.libraryWidget.replaceWidget(self.libraryPlaceholder)

    def showEvent(self, showEvent: QShowEvent):
        super().showEvent(showEvent)
        self.reloadStatistics()

    def reloadStatistics(self):
        tagFinder = TagFinder(settings.LIBRARY_PATH)
        tagNameToEntries = {
            tagName: list(tagFinder.genEntriesWithTag(tagName))
            for tagName in tagFinder.findAllTags()}

        self.tableWidget.clear()
        self.tableWidget.setRowCount(len(tagNameToEntries))

        for i, (tagName, tagEntries) in enumerate(sorted(
                tagNameToEntries.items(), key=lambda kv: -len(kv[1]))):
            tagFiles = '\n'.join(str(t.file) for t in tagEntries)
            row = (tagName, len(tagEntries), tagFiles)

            column: TagStatistics.TableColumn
            for column, val in zip(iter(self.TableColumn), row):
                item = QTableWidgetItem(str(val))
                item.setToolTip(str(val))
                self.tableWidget.setItem(i, column.value, item)

        for col in self.TableColumn:
            self.tableWidget.resizeColumnToContents(col.value)

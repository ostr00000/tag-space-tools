from PyQt5.QtWidgets import QTabWidget
from pyqt_utils.metaclass.geometry_saver import GeometrySaverMeta
from pyqt_utils.widgets.base_ui_widget import BaseWidget

from tag_space_tools.gui.duplicate.widget import DuplicateWidget
from tag_space_tools.gui.settings import tsSettings
from tag_space_tools.gui.statistics import TagStatistics
from tag_space_tools.gui.tag_fixer.fix_missing_tag_widget import FixMissingTagWidget
from tag_space_tools.gui.tag_rename import TagRename
from tag_space_tools.gui.tag_sorter.widget import TagSorter


class TagSpaceTabWidget(
    QTabWidget, BaseWidget, settings=tsSettings, metaclass=GeometrySaverMeta
):

    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self.tagSorterWidget = TagSorter(self)
        self.addTab(self.tagSorterWidget, "Sort tagged files")

        self.removeDup = DuplicateWidget(self)
        self.addTab(self.removeDup, "Remove duplicated files")

        self.fixMissingTagWidget = FixMissingTagWidget(self)
        self.addTab(self.fixMissingTagWidget, "Fix missing tag")

        self.tagRename = TagRename(self)
        self.addTab(self.tagRename, "Rename tag")

        self.statistics = TagStatistics(self)
        self.addTab(self.statistics, "Statistics")

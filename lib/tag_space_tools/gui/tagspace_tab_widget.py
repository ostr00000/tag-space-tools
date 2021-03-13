from PyQt5.QtWidgets import QTabWidget

from pyqt_utils.metaclass.geometry_saver import GeometrySaverMeta
from pyqt_utils.ui_base_widget import BaseWidget
from tag_space_tools.gui.fix_missing_tag_widget import FixMissingTagWidget
from tag_space_tools.gui.settings import settings
from tag_space_tools.gui.tag_sorter_widget import TagSorter


class TagSpaceTabWidget(BaseWidget, QTabWidget, settings=settings,
                        metaclass=GeometrySaverMeta.wrap(QTabWidget)):

    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self.fixMissingTagWidget = FixMissingTagWidget(self)
        self.addTab(self.fixMissingTagWidget, "Fix missing tag")

        self.tagSorterWidget = TagSorter(self)
        self.addTab(self.tagSorterWidget, "Sort tagged files")

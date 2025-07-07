from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from pyqt_utils.qobjects.display_widget_action import DisplayWidgetAction

from tag_space_tools.gui.tagspace_tab_widget import TagSpaceTabWidget


class PluginTagSpaceTools(DisplayWidgetAction[TagSpaceTabWidget]):
    sortOrder = 240

    def __init__(self, parent):
        icon = QIcon.fromTheme('tag_space_tools:tag_spaces_logo.png')
        super().__init__(icon=icon, text='Tag Space Tools', parent=parent)

    def createWidget(self, parent: QWidget | None = None) -> TagSpaceTabWidget:
        return TagSpaceTabWidget()

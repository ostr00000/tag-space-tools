from PyQt5.QtGui import QIcon
from pyqt_utils.qobjects.display_widget_action import DisplayWidgetAction
from tag_space_tools.gui.tagspace_tab_widget import TagSpaceTabWidget


class PluginTagSpaceTools(DisplayWidgetAction[TagSpaceTabWidget]):
    def __init__(self, parent):
        icon = QIcon.fromTheme('tagspaces')
        super().__init__(icon=icon, text='Tag Space Tools', parent=parent)

    def createWidget(self):
        return TagSpaceTabWidget()

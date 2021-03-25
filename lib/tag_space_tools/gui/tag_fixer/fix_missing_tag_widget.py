import logging
import traceback
from contextlib import contextmanager
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget

from pyqt_settings.field.base import Field
from pyqt_utils.metaclass.slot_decorator import SlotDecoratorMeta
from pyqt_utils.python.decorators import cursorDec
from pyqt_utils.widgets.base_widget import BaseWidget
from tag_space_tools.core import tagSpaceCoreName
from tag_space_tools.core.file_searcher import TagSpaceSearcher
from tag_space_tools.gui.settings import settings, TagSpacePluginSettings
from tag_space_tools.gui.tag_fixer.text_handler import TextEditHandler
from tag_space_tools.ui.ui_fix_widget import Ui_TagSpaceFixWidget

logger = logging.getLogger(__name__)


class FixMissingTagWidget(Ui_TagSpaceFixWidget, BaseWidget, QWidget, metaclass=SlotDecoratorMeta):

    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self.textHandler = TextEditHandler(self.textEdit, self.treeView, self.filterLine)

        self.fixButton.clicked.connect(self.onFixTagsClicked)
        self.advancedMode.clicked.connect(self.onAdvancedModeChanged)
        self.advancedMode.setCheckState(Qt.PartiallyChecked)

        field: Field = TagSpacePluginSettings.LIBRARY_PATH
        self.libraryWidget = field.createWidgetWithLabel(settings)
        self.libraryWidget.replaceWidget(self.libraryPlaceholder)

    def onSaveLibraryPath(self):
        settings.LIBRARY_PATH = self.libraryWidget.fieldWidget.getValue()

    @contextmanager
    def handleException(self):
        try:
            yield
        except Exception as exc:
            text = f'{exc}\n{traceback.format_exc()}'
            logger.error(text)
            self.textHandler.addText(text, QColor(Qt.red))
            QApplication.processEvents()

    @cursorDec
    def onFixTagsClicked(self):
        with self.handleException(), self.textHandler.useForLogger(tagSpaceCoreName):
            loc = settings.LIBRARY_PATH
            if not loc:
                loc = QFileDialog.getExistingDirectory(
                    caption="Select tag space root directory")

            if not (loc and Path(loc).exists()):
                return

            settings.LIBRARY_PATH = loc
            tss = TagSpaceSearcher(loc)
            tss.match()

    def onAdvancedModeChanged(self):
        state = self.advancedMode.checkState()
        self.groupTreeView.show()
        self.groupTextEdit.show()

        if state == Qt.Unchecked:
            self.groupTreeView.hide()
        elif state == Qt.Checked:
            self.groupTextEdit.hide()

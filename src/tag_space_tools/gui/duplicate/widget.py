import logging
import shlex
from pathlib import Path
from shutil import which

from PyQt5.QtCore import QItemSelectionModel, Qt, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMenu, QAction

from pyqt_settings.field.base import Field
from pyqt_utils.metaclass.geometry_saver import GeometrySaverMeta
from pyqt_utils.python.process_async import runProcessAsync
from pyqt_utils.widgets.base_widget import BaseWidget
from tag_space_tools.core.find_duplicates import findDuplicates
from tag_space_tools.gui.duplicate.dup_model import DupModel
from tag_space_tools.gui.duplicate.selection_delegate import DarkerSelectionDelegate
from tag_space_tools.gui.settings import settings, TagSpacePluginSettings
from tag_space_tools.ui.duplicate_widget_ui import Ui_DuplicateWidget

logger = logging.getLogger(__name__)


class DuplicateWidget(Ui_DuplicateWidget, BaseWidget, QWidget,
                      metaclass=GeometrySaverMeta.wrap(QWidget),
                      settings=settings):

    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        field: Field = TagSpacePluginSettings.LIBRARY_PATH
        self.libraryWidget = field.createWidgetWithLabel(settings)
        self.libraryWidget.replaceWidget(self.pathPlaceholder)

        self.model = DupModel()
        self.tableView.setItemDelegate(DarkerSelectionDelegate(self))
        self.tableView.setModel(self.model)
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.onCustomContextMenuRequested)

        self.findDuplicatesButton.clicked.connect(self.onFinDuplicatesClicked)
        self.selectCandidatesButton.clicked.connect(self.onSelectCandidates)
        self.removeSelectedButton.clicked.connect(self.onRemoveSelectionButton)

    def onCustomContextMenuRequested(self, pos: QPoint):
        showInFolder = QAction(QIcon.fromTheme('folder'), "Show in folder", self)

        @showInFolder.triggered.connect
        def onShowInFolderActionTriggered():
            index = self.tableView.indexAt(pos)
            path: Path = index.data(DupModel.PATH_ROLE)
            if which('dolphin') is not None:
                args = ['dolphin', '--select', str(path)]
                runProcessAsync(shlex.join(args), shell=True)
            else:
                args = ['xdg-open', str(path.parent)]
                runProcessAsync(args)

        menu = QMenu(self)
        menu.addAction(showInFolder)
        menu.popup(self.tableView.viewport().mapToGlobal(pos))

    def onFinDuplicatesClicked(self):
        path = settings.LIBRARY_PATH
        if not path:
            return

        dup = findDuplicates(path)
        self.model.setDupResult(dup)
        self.selectCandidatesButton.clicked.emit()

    def onSelectCandidates(self):
        selModel = self.tableView.selectionModel()
        selModel.clearSelection()
        for index in self.model.genSelectionCandidates():
            selModel.select(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)

    def onRemoveSelectionButton(self):
        for si in self.tableView.selectionModel().selectedRows():
            path: Path = si.data(DupModel.PATH_ROLE)
            try:
                path.unlink()
                logger.info(f"Removing file: {path}")
            except OSError as e:
                logger.exception(e)

        self.findDuplicatesButton.clicked.emit()

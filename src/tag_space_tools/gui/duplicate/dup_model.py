from collections.abc import Iterable

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QBrush, QColor
from pyqt_utils.python.late_init import LateInit

from tag_space_tools.core.find_duplicates import PathDupAggregator

_topLevelIndex = QModelIndex()


class DupModel(QAbstractTableModel):
    PATH_ROLE = Qt.UserRole

    rawData = LateInit[PathDupAggregator]()

    def __init__(self):
        super().__init__()
        self._modelData: list[list[str]] = []

    def setDupResult(self, dupResult: PathDupAggregator):
        self.beginResetModel()
        self.rawData = dupResult
        self._modelData = list(dupResult.getAllLevels())
        self.endResetModel()

    @classmethod
    def flatList[T](cls, *args: T | Iterable[T]) -> list[T]:
        res: list[T] = []
        for a in args:
            if isinstance(a, Iterable):
                b: Iterable[T] = a
                res.extend(cls.flatList(*b))
            else:
                res.append(a)
        return res

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole
    ):
        if not self._modelData:
            return None
        if orientation != Qt.Horizontal or role != Qt.DisplayRole:
            return None

        if section + 1 == len(self._modelData[0]):
            return "Duplicated file path"

        return f"Stage {section}"

    def rowCount(self, parent: QModelIndex = _topLevelIndex) -> int:
        return len(self._modelData)

    def columnCount(self, parent: QModelIndex = _topLevelIndex) -> int:
        if not self._modelData:
            return 0

        return len(self._modelData[0])

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if role in (Qt.DisplayRole, Qt.ToolTipRole):
            val = self._modelData[index.row()][index.column()]
            return str(val)

        if role == Qt.BackgroundRole:
            h = hash(tuple(self._modelData[index.row()][:-1]))
            color = QColor((h * 21) % 255, (h * 213) % 255, (h * 2137) % 255)
            return QBrush(color)

        if role == Qt.TextAlignmentRole:
            if index.column() == self.columnCount() - 1:
                return Qt.AlignRight
            return None

        if role == self.PATH_ROLE:
            return self._modelData[index.row()][-1]
        return None

    def genSelectionCandidates(self) -> Iterable[QModelIndex]:
        row = 0
        for values in self.rawData.getAllLevels():
            locSel = []
            for v in values:
                if 'sort' in str(v):
                    locSel.append(self.index(row, 0))
                row += 1

            if locSel and len(locSel) == len(values):
                del locSel[-1]
            yield from locSel

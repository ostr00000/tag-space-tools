from typing import Iterable

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QColor, QBrush

from tag_space_tools.core.find_duplicates import DUP_RESULT


class DupModel(QAbstractTableModel):
    PATH_ROLE = Qt.UserRole

    def __init__(self):
        super().__init__()
        self._modelData: list[tuple] = []
        self._rawData: DUP_RESULT = {}

    def setDupResult(self, dupResult: DUP_RESULT):
        self.beginResetModel()
        self._modelData = [self.flatTuple(k, v) for k, values in dupResult.items() for v in values]
        self._rawData = dupResult
        self.endResetModel()

    @classmethod
    def flatTuple(cls, *args) -> list:
        res = []
        for a in args:
            if isinstance(a, Iterable):
                res.extend(cls.flatTuple(*a))
            else:
                res.append(a)
        return res

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if not self._modelData:
            return
        if orientation != Qt.Horizontal or role != Qt.DisplayRole:
            return

        if section + 1 == len(self._modelData[0]):
            return "Duplicated file path"
        else:
            return f"Stage {section}"

    def rowCount(self, parent: QModelIndex = None) -> int:
        return len(self._modelData)

    def columnCount(self, parent: QModelIndex = None) -> int:
        if not self._modelData:
            return 0
        else:
            return len(self._modelData[0])

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            val = self._modelData[index.row()][index.column()]
            return str(val)

        elif role == Qt.BackgroundRole:
            h = hash(tuple(self._modelData[index.row()][:-1]))
            color = QColor((h * 21) % 255, (h * 213) % 255, (h * 2137) % 255)
            return QBrush(color)

        elif role == Qt.TextAlignmentRole:
            if index.column() == self.columnCount() - 1:
                return Qt.AlignRight

        elif role == self.PATH_ROLE:
            return self._modelData[index.row()][-1]

    def genSelectionCandidates(self) -> Iterable[QModelIndex]:
        row = 0
        for values in self._rawData.values():
            locSel = []
            for v in values:
                if 'sort' in str(v):
                    locSel.append(self.index(row, 0))
                row += 1

            if locSel and len(locSel) == len(values):
                del locSel[-1]
            yield from locSel

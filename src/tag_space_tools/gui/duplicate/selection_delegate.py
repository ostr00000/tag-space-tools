from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QPainter, QBrush, QPalette, QColor
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QStyle


class DarkerSelectionDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        if option.state & QStyle.State_Selected:
            brush: QBrush = index.data(Qt.BackgroundRole)
            if brush is not None:
                c = brush.color()
                color = QColor(255 - c.red(), 255 - c.green(), 255 - c.blue())
                option.palette.setColor(QPalette.Highlight, color)
                option.palette.setColor(QPalette.HighlightedText, Qt.black)

        super().paint(painter, option, index)

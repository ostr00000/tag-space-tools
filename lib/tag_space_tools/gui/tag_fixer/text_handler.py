from __future__ import annotations

import logging
import re
from contextlib import contextmanager
from itertools import takewhile
from typing import Optional, Dict, List

from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QColor, QTextCursor, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTextEdit, QTreeView, QLineEdit


@contextmanager
def changeColor(textEdit: QTextEdit, color: Optional[QColor] = None):
    if color is None:
        yield
    else:
        oldColor = textEdit.textColor()
        textEdit.setTextColor(color)
        yield
        textEdit.setTextColor(oldColor)


class TextEditHandler(logging.Handler):
    colorMap = {
        logging.DEBUG: Qt.gray,
        logging.INFO: Qt.green,
        logging.WARNING: Qt.darkYellow,
        logging.ERROR: Qt.red,
    }

    PREFIX_MAX_SIZE = 30
    VALID_PREFIX = re.compile(r'[^\w ]')

    @contextmanager
    def useForLogger(self, loggerName: str):
        self.reset()
        tagLogger = logging.getLogger(loggerName)
        tagLogger.addHandler(self)
        yield
        tagLogger.removeHandler(self)

    def __init__(self, textEdit: QTextEdit, treeView: QTreeView, filterLineEdit: QLineEdit = None):
        super().__init__()
        self.treeView = treeView
        self.textEdit = textEdit
        self.filterLineEdit = filterLineEdit

        self.model = QStandardItemModel(self.treeView)
        self.filterModel = QSortFilterProxyModel(self.treeView)
        self.filterModel.setSourceModel(self.model)
        self.filterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filterModel.setRecursiveFilteringEnabled(True)
        self.treeView.setModel(self.filterModel)

        if self.filterLineEdit is not None:
            self.filterLineEdit.textChanged.connect(self.filterModel.setFilterRegExp)
        self.treeView.setHeaderHidden(True)

        self.topItem = None
        self._groups: List[str] = []
        self._prefix: Dict[str, QStandardItem] = {}
        self.reset()

    def reset(self):
        self.model.clear()
        self.topItem = QStandardItem('Top Item')
        self.model.setItem(0, 0, self.topItem)
        self._groups.clear()
        self._prefix.clear()

    def emit(self, record: logging.LogRecord):
        msg = self.format(record)
        color = self.colorMap.get(record.levelno, Qt.black)
        self.addText(msg, color)
        self.addGroup(msg)
        self.treeView.expandToDepth(0)

    def addText(self, text: str, color: QColor = None):
        with changeColor(self.textEdit, color):
            self.textEdit.insertPlainText(text + '\n')
            self.textEdit.moveCursor(QTextCursor.End)

    def addGroup(self, text: str):
        self._groups.append(text)
        validPrefix = self.VALID_PREFIX.split(text, maxsplit=1)[0]

        item = QStandardItem(text)
        if existingItem := self._findItemWithExistingPrefix(validPrefix):
            parentItem = existingItem

        elif biggestPrefix := self._getBiggestCommonPrefix(validPrefix):
            assert biggestPrefix is not None
            item, biggestPrefixText, prefixSize = biggestPrefix

            parentItem = self._addPrefix(validPrefix, prefixSize)
            self._moveItems(parentItem, validPrefix)

        else:
            parentItem = self._addPrefix(validPrefix)

        parentItem.appendRow(item)

    def _findItemWithExistingPrefix(self, text: str):
        for prefix, item in self._prefix.items():
            if item.text().startswith(text):
                return item

        return None

    def _getBiggestCommonPrefix(self, text):
        keyToPrefix: Dict[str, int] = {
            group: sum(1 for _ in takewhile(lambda x: x[0] == x[1], zip(text, group)))
            for group in self._groups
        }
        if not (biggestPrefix := max(keyToPrefix, key=keyToPrefix.get, default=None)):
            return

        for i in range(self.topItem.rowCount()):
            prefixItem = self.topItem.child(i, 0)
            if prefixItem.text() == biggestPrefix:
                return prefixItem, biggestPrefix, keyToPrefix[biggestPrefix]

        return None

    def _addPrefix(self, text, size=None):
        if size is None:
            size = self.PREFIX_MAX_SIZE

        validPrefix = self.VALID_PREFIX.split(text, maxsplit=1)[0]
        prefix = validPrefix[:size]
        self._prefix[prefix] = parentItem = QStandardItem(prefix)
        self.topItem.appendRow(parentItem)
        return parentItem

    def _moveItems(self, newItem: QStandardItem, prefix: str):
        for i in reversed(range(self.topItem.rowCount())):
            child = self.topItem.child(i, 0)
            if child.text().startswith(prefix):
                self.topItem.takeChild(i, 0)
                newItem.appendRow(child)

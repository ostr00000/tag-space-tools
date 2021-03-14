import json
from pathlib import Path
from typing import Iterable

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor, QDropEvent
from PyQt5.QtWidgets import QListWidgetItem, QListWidget

from tag_space_tools.core.tag_space_entry import Tag


class TagItem(QListWidgetItem):
    def __init__(self, tag: Tag, parent=None):
        super().__init__(tag.title, parent=parent)
        self.tag = tag
        self.setBackground(self._convertColor(tag.color))
        self.setForeground(self._convertColor(tag.textcolor))

    @staticmethod
    def _convertColor(color: str) -> QColor:
        if color.startswith('#'):
            colorRgb = color[:7]
            return QColor(colorRgb)
        else:
            return QColor(color)


class TagListWidget(QListWidget):
    dataChanged = pyqtSignal()

    def replaceTags(self, tags: Iterable[Tag]):
        self.clear()
        self.addItems(tags)

    def addItems(self, tags: Iterable[Tag]):
        for t in tags:
            self.addItem(TagItem(t))
        self.dataChanged.emit()

    def removeSelected(self):
        for item in reversed(self.selectedItems()):
            row = self.row(item)
            self.takeItem(row)
        self.dataChanged.emit()

    def getSortTags(self) -> list[Tag]:
        sortTags = []
        for i in range(self.count()):
            item = self.item(i)
            assert isinstance(item, TagItem)
            sortTags.append(item.tag)
        return sortTags

    def saveToFile(self, savePath):
        Path(savePath).parent.mkdir(parents=True, exist_ok=True)
        with open(savePath, 'w') as saveFile:
            serialized = json.dumps(
                self.getSortTags(), default=lambda x: x.__dict__)
            saveFile.write(serialized)

    def dropEvent(self, event: QDropEvent):
        super().dropEvent(event)
        if event.isAccepted():
            self.dataChanged.emit()

import json
from collections.abc import Iterable
from pathlib import Path

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor, QDropEvent
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

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
        return QColor(color)


class TagListWidget(QListWidget):
    dataChangedSig = pyqtSignal()

    def updateTags(self, newTags: Iterable[Tag]):
        """Remove existing tags that are not in `newTag` and set `newTags`."""
        newTags = list(newTags)
        for i in reversed(range(self.count())):
            item = self.item(i)
            if not isinstance(item, TagItem):
                raise TypeError

            try:
                newTags.remove(item.tag)
            except ValueError:
                self.takeItem(i)

        self.addItems(newTags)

    def addItems(self, tags: Iterable[Tag]):
        for t in tags:
            self.addItem(TagItem(t))
        self.dataChangedSig.emit()

    def removeSelected(self):
        for item in reversed(self.selectedItems()):
            row = self.row(item)
            self.takeItem(row)
        self.dataChangedSig.emit()

    def getAllTags(self) -> list[Tag]:
        sortTags = []
        for i in range(self.count()):
            item = self.item(i)
            if not isinstance(item, TagItem):
                raise TypeError
            sortTags.append(item.tag)
        return sortTags

    def saveToFile(self, savePath: str | Path):
        sp = Path(savePath)
        sp.parent.mkdir(parents=True, exist_ok=True)
        with sp.open('w') as saveFile:
            serialized = json.dumps(self.getAllTags(), default=lambda x: x.__dict__)
            saveFile.write(serialized)

    def dropEvent(self, event: QDropEvent):
        super().dropEvent(event)
        if event.isAccepted():
            self.dataChangedSig.emit()

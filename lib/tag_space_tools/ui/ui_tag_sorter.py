# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/tag_sorter.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TagSorter(object):
    def setupUi(self, TagSorter):
        TagSorter.setObjectName("TagSorter")
        TagSorter.resize(527, 519)
        self.gridLayout_2 = QtWidgets.QGridLayout(TagSorter)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(TagSorter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.loadTagsButton = QtWidgets.QToolButton(TagSorter)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.loadTagsButton.setIcon(icon)
        self.loadTagsButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.loadTagsButton.setObjectName("loadTagsButton")
        self.horizontalLayout.addWidget(self.loadTagsButton)
        self.saveButton = QtWidgets.QToolButton(TagSorter)
        icon = QtGui.QIcon.fromTheme("document-save-as")
        self.saveButton.setIcon(icon)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.removeTagButton = QtWidgets.QToolButton(TagSorter)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.removeTagButton.setIcon(icon)
        self.removeTagButton.setObjectName("removeTagButton")
        self.horizontalLayout.addWidget(self.removeTagButton)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.listWidget = TagListWidget(TagSorter)
        self.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 6, 1)
        self.moveFilesButton = QtWidgets.QPushButton(TagSorter)
        self.moveFilesButton.setObjectName("moveFilesButton")
        self.gridLayout_2.addWidget(self.moveFilesButton, 4, 2, 1, 1)
        self.fromFolderPlaceholder = QtWidgets.QPushButton(TagSorter)
        self.fromFolderPlaceholder.setObjectName("fromFolderPlaceholder")
        self.gridLayout_2.addWidget(self.fromFolderPlaceholder, 2, 2, 1, 1)
        self.toFolderPlaceholder = QtWidgets.QPushButton(TagSorter)
        self.toFolderPlaceholder.setObjectName("toFolderPlaceholder")
        self.gridLayout_2.addWidget(self.toFolderPlaceholder, 3, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 294, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 5, 2, 1, 1)
        self.maxFilesPlaceholder = QtWidgets.QPushButton(TagSorter)
        self.maxFilesPlaceholder.setObjectName("maxFilesPlaceholder")
        self.gridLayout_2.addWidget(self.maxFilesPlaceholder, 1, 2, 1, 1)

        self.retranslateUi(TagSorter)
        QtCore.QMetaObject.connectSlotsByName(TagSorter)

    def retranslateUi(self, TagSorter):
        _translate = QtCore.QCoreApplication.translate
        TagSorter.setWindowTitle(_translate("TagSorter", "Form"))
        self.label.setText(_translate("TagSorter", "Tag order:"))
        self.loadTagsButton.setText(_translate("TagSorter", "Load tag library"))
        self.saveButton.setText(_translate("TagSorter", "..."))
        self.removeTagButton.setText(_translate("TagSorter", "Remove"))
        self.moveFilesButton.setText(_translate("TagSorter", "Move files"))
        self.fromFolderPlaceholder.setText(_translate("TagSorter", "From folder placeholder"))
        self.toFolderPlaceholder.setText(_translate("TagSorter", "To folder placeholder"))
        self.maxFilesPlaceholder.setText(_translate("TagSorter", "Max files placeholder"))
from tag_space_tools.gui.tag_sorter.list_widget import TagListWidget

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/tag_rename.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TagRename(object):
    def setupUi(self, TagRename):
        TagRename.setObjectName("TagRename")
        TagRename.resize(611, 449)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(TagRename)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(TagRename)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.fromComboBox = QtWidgets.QComboBox(TagRename)
        self.fromComboBox.setObjectName("fromComboBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fromComboBox)
        self.label_2 = QtWidgets.QLabel(TagRename)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.toLineEdit = QtWidgets.QLineEdit(TagRename)
        self.toLineEdit.setObjectName("toLineEdit")
        self.horizontalLayout.addWidget(self.toLineEdit)
        self.toComboBox = QtWidgets.QComboBox(TagRename)
        self.toComboBox.setObjectName("toComboBox")
        self.horizontalLayout.addWidget(self.toComboBox)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.renameButton = QtWidgets.QPushButton(TagRename)
        self.renameButton.setObjectName("renameButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.renameButton)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.splitter = QtWidgets.QSplitter(TagRename)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.textEdit = QtWidgets.QTextEdit(self.splitter)
        self.textEdit.setObjectName("textEdit")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.filterLineEdit = QtWidgets.QLineEdit(self.widget)
        self.filterLineEdit.setObjectName("filterLineEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.filterLineEdit)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.treeView = QtWidgets.QTreeView(self.widget)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.verticalLayout_2.addWidget(self.splitter)
        self.libraryPlaceholder = QtWidgets.QPushButton(TagRename)
        self.libraryPlaceholder.setObjectName("libraryPlaceholder")
        self.verticalLayout_2.addWidget(self.libraryPlaceholder)

        self.retranslateUi(TagRename)
        QtCore.QMetaObject.connectSlotsByName(TagRename)

    def retranslateUi(self, TagRename):
        _translate = QtCore.QCoreApplication.translate
        TagRename.setWindowTitle(_translate("TagRename", "Tag rename"))
        self.label.setText(_translate("TagRename", "From tag:"))
        self.label_2.setText(_translate("TagRename", "To tag:"))
        self.renameButton.setText(_translate("TagRename", "Rename"))
        self.label_3.setText(_translate("TagRename", "Filter:"))
        self.libraryPlaceholder.setText(_translate("TagRename", "Library placeholder"))

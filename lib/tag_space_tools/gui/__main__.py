import logging

from PyQt5.QtWidgets import QTabWidget

from tag_space_tools import moduleName, appName, appDisplayName, orgName
from tag_space_tools.gui.tag_sorter import TagSorter


# noinspection DuplicatedCode
def main():
    logging.basicConfig(level=logging.DEBUG)
    mainLogger = logging.getLogger(moduleName)
    mainLogger.setLevel(logging.DEBUG)

    from PyQt5.QtWidgets import QApplication
    from tag_space_tools.gui.fix_dialog import FixDialog

    app = QApplication([])
    app.setApplicationName(appName)
    app.setOrganizationName(orgName)
    app.setApplicationDisplayName(appDisplayName)

    tabWidget = QTabWidget()
    tabWidget.addTab(FixDialog(tabWidget), "Tag fixer")
    tabWidget.addTab(TagSorter(tabWidget), "Tag sorter")
    tabWidget.show()
    app.exec()


if __name__ == '__main__':
    main()

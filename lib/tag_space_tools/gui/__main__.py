import logging

from tag_space_tools import moduleName, appName, appDisplayName, orgName
from tag_space_tools.gui.tagspace_tab_widget import TagSpaceTabWidget


# noinspection DuplicatedCode
def main():
    logging.basicConfig(level=logging.DEBUG)
    mainLogger = logging.getLogger(moduleName)
    mainLogger.setLevel(logging.DEBUG)

    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    app.setApplicationName(appName)
    app.setOrganizationName(orgName)
    app.setApplicationDisplayName(appDisplayName)

    tabWidget = TagSpaceTabWidget()
    tabWidget.show()
    app.exec()


if __name__ == '__main__':
    main()

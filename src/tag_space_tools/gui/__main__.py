import logging

from PyQt5.QtWidgets import QApplication

from tag_space_tools import appDisplayName, appName, orgName, packageName


def prepareLoggers():
    logging.basicConfig(level=logging.DEBUG)
    mainLogger = logging.getLogger(packageName)
    mainLogger.setLevel(logging.DEBUG)


def main():
    from tag_space_tools.gui.tagspace_tab_widget import (  # noqa:PLC0415
        TagSpaceTabWidget,
    )

    app = QApplication([])
    app.setApplicationName(appName)
    app.setOrganizationName(orgName)
    app.setApplicationDisplayName(appDisplayName)

    tabWidget = TagSpaceTabWidget()
    tabWidget.show()
    app.exec()


if __name__ == '__main__':
    prepareLoggers()
    main()

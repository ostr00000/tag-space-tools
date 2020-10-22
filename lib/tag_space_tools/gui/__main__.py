import logging

from tag_space_tools import moduleName, appName, appDisplayName, orgName


def main():
    logging.basicConfig(level=logging.DEBUG)
    mainLogger = logging.getLogger(moduleName)
    mainLogger.setLevel(logging.DEBUG)

    from PyQt5.QtWidgets import QApplication
    from tag_space_tools.gui.dialog import FixDialog

    app = QApplication([])
    app.setApplicationName(appName)
    app.setOrganizationName(orgName)
    app.setApplicationDisplayName(appDisplayName)

    fd = FixDialog()
    fd.show()
    app.exec()


if __name__ == '__main__':
    print('main')
    main()

import os
from pathlib import Path

from PyQt5.QtCore import QDir

modulePath = os.path.dirname(__file__)
packageName = __name__
appName = "tag-space-tools"
appDisplayName = "Tag space tools"
orgName = 'ostr00000'

resourcePath = Path(__file__).resolve().parent / 'resources'
assert resourcePath.exists()
QDir.addSearchPath(packageName, str(resourcePath))

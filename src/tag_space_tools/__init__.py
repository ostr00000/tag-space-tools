from pathlib import Path

from PyQt5.QtCore import QDir

modulePath = Path(__file__).resolve().parent
packageName = __name__
appName = "tag-space-tools"
appDisplayName = "Tag space tools"
orgName = 'ostr00000'

resourcePath = modulePath / "resources"
if not resourcePath.exists():
    _msg = "Cannot find resources directory"
    raise FileNotFoundError(_msg)

QDir.addSearchPath(packageName, str(resourcePath))

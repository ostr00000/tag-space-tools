from PyQt5.QtCore import QSettings

from pyqt_settings.field.string import StrField


class TagSpacePluginSettings(QSettings):
    LAST_PATH = StrField('fix_tag/last_path', default='')


settings = TagSpacePluginSettings('ostr00000', 'tag-space-tools')

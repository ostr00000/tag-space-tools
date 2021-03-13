import json

from PyQt5.QtCore import QSettings

from pyqt_settings.field.integer import IntField
from pyqt_settings.field.list import ListField
from pyqt_settings.field.string import StrField


class TagSpacePluginSettings(QSettings):
    LAST_PATH = StrField('fix_tag/last_path', default='')

    LIBRARY_PATH = StrField('tag_sorter/tag_library')
    FROM_PATH = StrField('tag_sorter/from_path')
    TO_PATH = StrField('tag_sorter/to_path')
    MAX_FILES_PER_LEVEL = IntField('tag_sorter/max_files_per_level', default=20)
    SORTED_TAGS = ListField('tag_sorter/sorted_tags', castType=json.loads)


settings = TagSpacePluginSettings('ostr00000', 'tag-space-tools')

from PyQt5.QtCore import QSettings

from pyqt_settings.field.integer import IntField
from pyqt_settings.field.json import JsonField
from pyqt_settings.field.string import StrField
from tag_space_tools.core.tag_space_entry import Tag


class TagSpacePluginSettings(QSettings):
    LAST_PATH = StrField('fix_tag/last_path', default='')

    LIBRARY_PATH = StrField('tag_sorter/tag_library')
    FROM_PATH = StrField('tag_sorter/from_path')
    TO_PATH = StrField('tag_sorter/to_path')
    MAX_FILES_PER_LEVEL = IntField('tag_sorter/max_files_per_level', default=20)
    SORTED_TAGS = JsonField('tag_sorter/sorted_tags', castTypes=(list, Tag.fromDict))
    LAST_SAVE_FILE = StrField('tag_sorter/last_save_file')


settings = TagSpacePluginSettings('ostr00000', 'tag-space-tools')

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QFileDialog
from pyqt_settings.factory.base import ConfigFunc, WidgetFactory
from pyqt_settings.field.json_field import JsonField
from pyqt_settings.field.simple import IntField, PathField
from pyqt_settings.gui_widget.path_line_edit import PathLineEdit

from tag_space_tools.core.tag_space_entry import TagsSerializer


class TagSpacePluginSettings(QSettings):
    LIBRARY_PATH = PathField('common/library_path')
    LIBRARY_PATH.widgetFactory = WidgetFactory(
        PathLineEdit,
        configFunctions=[
            ConfigFunc(QFileDialog.setWindowTitle, "Select main library folder"),
            ConfigFunc(QFileDialog.setFileMode, QFileDialog.Directory),
        ],
    )

    SORT_FILE_LIBRARY = PathField('tag_sorter/tag_library')

    UNSORTED_PATH = PathField('tag_sorter/from_path')
    UNSORTED_PATH.widgetFactory = WidgetFactory(
        PathLineEdit,
        configFunctions=[
            ConfigFunc(QFileDialog.setWindowTitle, "Select folder with unsorted files"),
            ConfigFunc(QFileDialog.setFileMode, QFileDialog.Directory),
        ],
    )

    MAX_FILES_PER_LEVEL = IntField('tag_sorter/max_files_per_level', default=20)
    SORTED_TAGS = JsonField(
        'tag_sorter/sorted_tags',
        castType=TagsSerializer.deserialize,
        jsonSerializeFun=TagsSerializer.serialize,
    )
    LAST_SAVE_FILE = PathField('tag_sorter/last_save_file')


tsSettings = TagSpacePluginSettings('ostr00000', 'tag-space-tools')

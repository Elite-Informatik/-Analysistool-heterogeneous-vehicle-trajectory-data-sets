import sys as sys
from typing import Dict
from typing import List
from typing import Type

from src.data_transfer.content.column import Column
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.settings_record import SettingsRecord
from src.model.error_handler import ErrorHandler
from src.model.error_handler import ErrorMessage
from src.model.setting_structure.isetting_structure import ISettingStructure
from src.model.setting_structure.page import Page
from src.model.setting_structure.segment import Segment
from src.model.setting_structure.setting import Setting
from src.model.setting_structure.setting_type import Color
from src.data_transfer.content.settings_enum import SettingsEnum
from src.model.setting_structure.setting_tips import SettingTips


MIN_COLOR = 0
MAX_COLOR = sys.maxsize
DEF_COLOR = 0xDF2222

EXPORTABLE_SETTING_TYPES: List[Type] = [str, int, float]
STANDARD_PAGE_SIZE: int = 10


class SettingStructure(ErrorHandler, ISettingStructure):
    """
    The class responsible for managing the settings of the application.
    It stores a list of Pages, which consist of Segments, which in turn consist of Settings.
    """

    def __init__(self):
        """
        Initializes a new instance of the SettingStructure class. This class is responsible for
        managing the settings of the application.
        It stores a list of Pages, which consist of Segments, which in turn consist of Settings.
        """
        super().__init__()

        self._trajectory_percent: Setting = Setting.from_interval(identifier=SettingsEnum.TRAJECTORY_SAMPLE_SIZE,
                                                                  name="Number of Trajectories",
                                                                  standard=5, minimum=0, maximum=sys.maxsize,
                                                                  tip=SettingTips.TRAJECTORY_SAMPLE_SIZE.value)

        self._step_size: Setting = Setting.from_interval(identifier=SettingsEnum.TRAJECTORY_STEP_SIZE,
                                                         name="Trajectories datapoint step size",
                                                         standard=5, minimum=1, maximum=sys.maxsize,
                                                         tip=SettingTips.TRAJECTORY_STEP_SIZE.value)

        self._show_line_segments: Setting = Setting.boolean_setting(identifier=SettingsEnum.SHOW_LINE_SEGMENTS,
                                                              name="Show line segments",
                                                                    tip=SettingTips.SHOW_LINE_SEGMENTS.value)

        self._color: Setting = Setting.from_list(identifier=SettingsEnum.COLOR_SETTINGS, name="Trajectory Colors",
                                                 option_list=[color for color in Color], standard=Color.RANDOM,
                                                 tip=SettingTips.COLOR_SETTINGS.value)

        self._trajectory_uni_color: Setting = Setting.from_interval(identifier=SettingsEnum.TRAJECTORY_UNI_COLOR,
                                                                    name="Uni Color for trajectories",
                                                                    standard=DEF_COLOR,
                                                                    minimum=MIN_COLOR, maximum=MAX_COLOR,
                                                                    tip=SettingTips.TRAJECTORY_UNI_COLOR.value)

        self._trajectory_param_color: Setting = Setting.from_list(identifier=SettingsEnum.TRAJECTORY_PARAM_COLOR,
                                                                  name="Parameter Color for  trajectories",
                                                                  option_list=Column.get_number_interval_columns(),
                                                                  standard=Column.get_number_interval_columns()[0],
                                                                  tip=SettingTips.TRAJECTORY_PARAM_COLOR.value)

        self._filter_greyed_out: Setting = Setting.boolean_setting(identifier=SettingsEnum.FILTER_GREYED,
                                                                   name="Filter greyed out",
                                                                   tip=SettingTips.FILTER_GREYED.value)

        self._offset_ratio: Setting = Setting.from_interval(identifier=SettingsEnum.OFFSET, name="Offset ratio",
                                                            standard=0, minimum=0, maximum=1,
                                                            tip=SettingTips.OFFSET.value)

        self._random: Setting = Setting.boolean_setting(identifier=SettingsEnum.RANDOM_SAMPLE, name="Random sample",
                                                        tip=SettingTips.RANDOM_SAMPLE.value)

        self._seed: Setting = Setting.from_interval(identifier=SettingsEnum.RANDOM_SEED, name="Random seed",
                                                    standard=0, minimum=0, maximum=sys.maxsize,
                                                    tip=SettingTips.RANDOM_SEED.value)

        self._pages = [Page(SettingsEnum.PAGE1, "Trajectory Settings", []),
                       Page(SettingsEnum.PAGE2, "Color Settings", []),
                       Page(SettingsEnum.PAGE3, "Filter Settings", [])]
        trajectory_segment = Segment(SettingsEnum.SEGMENT1, "Trajectories", [])
        trajectory_segment.add_setting(self._trajectory_percent)
        trajectory_segment.add_setting(self._step_size)
        trajectory_segment.add_setting(self._offset_ratio)
        trajectory_segment.add_setting(self._random)
        trajectory_segment.add_setting(self._seed)
        self._pages[0].add_segment(trajectory_segment)

        color_segment = Segment(SettingsEnum.SEGMENT2, "Color", [])
        color_segment.add_setting(self._color)
        color_segment.add_setting(self._trajectory_param_color)
        color_segment.add_setting(self._trajectory_uni_color)
        color_segment.add_setting(self._show_line_segments)
        self._pages[1].add_segment(color_segment)

        filter_segment = Segment(SettingsEnum.SEGMENT3, "Filter", [])
        filter_segment.add_setting(self._filter_greyed_out)

        self._pages[2].add_segment(filter_segment)

    def add_page(self, name: str, identifier: SettingsEnum) -> bool:

        for page in self._pages:
            if page.get_identifier() == identifier:
                self.throw_error(ErrorMessage.PAGE_NOT_ADDED)
                return False
        self._pages.append(Page(identifier, name, []))

    def add_segment(self, name: str, identifier: SettingsEnum, page_identifier: SettingsEnum) -> bool:

        for page in self._pages:
            if page.get_identifier() == page_identifier:
                if page.create_segment(identifier=identifier, name=name):
                    return True
                break
        self.throw_error(ErrorMessage.SEGMENT_NOT_ADDED)
        return False

    def add_settings(self, page_identifier: SettingsEnum,
                     segment_identifier: SettingsEnum,
                     identifier: SettingsEnum,
                     name: str,
                     selection: SelectionRecord) -> bool:

        for page in self._pages:
            if page.get_identifier() == page_identifier:
                if page.create_setting(identifier=identifier, name=name, selection=selection,
                                       segment_identifier=segment_identifier):
                    return True
                break
        self.throw_error(ErrorMessage.SETTING_NOT_ADDED)
        return False

    def get_dictionary(self) -> dict:

        export_dict: Dict = {}
        for pages in self._pages:
            pages.export_to_dict(export_dict)
        return export_dict

    def load_from_dictionary(self, setting_dictionary: dict) -> bool:

        for pages in self._pages:
            pages.load_from_dict(setting_dictionary)
        return True

    def get_settings_record(self) -> SettingsRecord:
        return SettingsRecord(tuple(page.get_record() for page in self._pages))

    def update_settings(self, settings: SettingsRecord) -> bool:

        assert isinstance(settings, SettingsRecord)
        if not settings.equal_structure(self.get_settings_record()):
            self.throw_error(ErrorMessage.SETTING_NOT_MATCHING)
            return False
        self._pages = list(Page.from_record(page_record) for page_record in settings.pages)
        return True

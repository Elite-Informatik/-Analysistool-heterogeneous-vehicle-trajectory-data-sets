from enum import Enum


class SettingsEnum(Enum):
    """Enum for settings."""
    # PAGES
    PAGE1 = "page1"
    PAGE2 = "page2"
    PAGE3 = "page3"

    # SEGMENTS
    SEGMENT1 = "segment1"
    SEGMENT2 = "segment2"
    SEGMENT3 = "segment3"

    # SETTINGS
    SETTING1 = "setting1"
    SETTING2 = "setting2"
    SETTING3 = "setting3"
    TRAJECTORY_VIEW_STEP_SIZE = "trajectory_view_step_size"
    DEF_SETTING = "def_setting"
    TRAJECTORY_SAMPLE_SIZE = "trajectory_view_sample"
    TRAJECTORY_STEP_SIZE = "trajectory_view_step_size"
    SHOW_LINE_SEGMENTS = "show_line_segments"
    COLOR_SETTINGS = "color_settings"
    TRAJECTORY_UNI_COLOR = "trajectory_uni_color"
    TRAJECTORY_PARAM_COLOR = "trajectory_param_color"
    FILTER_GREYED = "filter_greyed"
    OFFSET = "offset"
    RANDOM_SAMPLE = "random_sample"
    RANDOM_SEED = "random_seed"

    INTERVAL = "INTERVAL"
    COLUMN = "COLUMN"
    DISCRETE = "DISCRETE"
    POLYGON = "POLYGON"

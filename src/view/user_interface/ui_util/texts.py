from enum import Enum


class EnglishTexts(Enum):
    """
    Enum that holds all text that are statically used in the user interface.
    """
    START_WINDOW_QUESTION = "What would you like to do?"
    NO_DATASET_IMPORTED_YET = "Please import dataset before you can select a dataset"
    ENTER_PATH = "enter path"
    CHOOSE_NAME_DATASET = "dataset name"
    START_WINDOW_TITLE = "Analysis Tool For Heterogeneous Vehicle Trajectory Datasets"
    MAIN_WINDOW_TITLE = "Analysis Tool For Heterogeneous Vehicle Trajectory Datasets"
    DATASET_WINDOW_TITLE = "Datasets"
    SETTINGS_WINDOW_TITLE = "Settings"
    MANUAL_WINDOW_TITLE = "Manual"
    DATASET_DELETE_SURE = "Are you sure you want to delete the following dataset?"

    # analysis view
    EXPORT_ANALYSIS_DIALOG_TITLE = "Export analysis"
    CREATE_ANALYSIS_DIALOG_TITLE = "Create analysis"
    IMPORT_ANALYSIS_DIALOG_TITLE = "Import analysis"
    CHANGE_ANALYSIS_DIALOG_TITLE = "Change analysis"
    CREATE_ANALYSIS_BTN_NAME = "create analysis"
    EXPORT_ANALYSIS_BTN_NAME = "export"
    REFRESH_ANALYSIS_BTN_NAME = "refresh"
    DELETE_ANALYSIS_BTN_NAME = "delete"
    CHANGE_ANALYSIS_BTN_NAME = "change"
    IMPORT_ANALYSIS_BTN_NAME = "import analysis"

    ERROR_NO_ANALYSIS_VIEW_FOUND = "Error: no analysis found"
    INSTRUCTION_NO_ANALYSIS_VIEW_FOUND = "Please create an analysis first!"
    INSTRUCTION_ENTER_EXPORT_FORMAT = "Select an export format:"
    INSTRUCTION_ENTER_DIRECTORY = "Select directory:"
    INSTRUCTION_SELECT_ANALYSIS_TYPE = "Select analysis type:"
    DEFAULT_ANALYSIS_NAME = "analysis"

    # selection view
    SELECTION_AMOUNT_RANGE_INSTRUCTION = "enter {start}-{end} values"
    SELECTION_ONE_ENTRY_INSTRUCTION = "enter one value"
    SELECTION_VALUE_RANGE_INSTRUCTION = "between {start} and {end} separated by '{separator}'"
    SELECTION_SEPARATOR = ","
    ERROR_INVALID_INPUT = "Invalid Input"
    INSTRUCTION_INVALID_INPUT = "Please check your input!"
    INSTRUCTION_ENTER_FILE_NAME = "Enter the file name:"
    USER_REQUEST_DIALOG_NAME = "request"

    # dialogs
    EXPORT_DATASET_DIALOG_NAME = "export dataset"
    IMPORT_DATASET_DIALOG_NAME = "import dataset"
    OPEN_DATASET_DIALOG_NAME = "open dataset"
    EXPORT_MAP_DIALOG_NAME = "export map"
    INVALID_FILE_PATH = "{} is an invalid file path"
    INVALID_DATASET_NAME = "Invalid dataset name.\nThe name can only contain lower case letters and numbers"
    EDIT_DISCRETE_FILTER_DIALOG_NAME = "Edit Discrete Filter"
    CREATE_DISCRETE_FILTER_DIALOG_NAME = "Create Discrete Filter"
    EDIT_FILTER_GROUP_DIALOG_NAME = "Edit Filter Group"
    CREATE_FILTER_GROUP_DIALOG_NAME = "Create Filter Group"

    # manual
    ANALYSIS_MANUAL_TITLE = "Analysis"
    FILTER_MANUAL_TITLE = "Filters"
    DATASET_MANUAL_TITLE = "Datasets"
    MAP_MANUAL_TITLE = "Map"
    POLYGON_MANUAL_TITLE = "Polygons"
    DATAFORMAT_MANUAL_TITLE = "Uniform dataformat"

    # general
    OK_BTN_NAME = "OK"
    CANCEL_BTN_NAME = "Cancel"
    SELECT_DIRECTORY_BTN_NAME = "Select directory"
    SELECT_PATH_BTN_NAME = "Select path"

    # tool tips
    IMPORT_DATASET_TIP = "Click the button to select a data format and paths of a new dataset. " \
                         "The dataset must be named. After the dataset was imported you can open " \
                         "it via the open dataset button."

    OPEN_DATASET_TIP = "Click the button to select the dataset you want to start the application with"
    SIDEBAR_TIP = "Right click to add a filter or filter group"
    POLYGON_BAR_TIP = "Right click on a polygon to delete a polygon"
    PLUS_P_TIP = "Click to enable polygon creation mode. If enabled you can draw polygons on the map"
    MINUS_P_TIP = "Click to enter polygon deletion mode. If enabled you can delete polygons by clicking them on the map"

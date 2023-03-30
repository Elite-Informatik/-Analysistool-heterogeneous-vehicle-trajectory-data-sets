from enum import Enum


class ErrorMessage(Enum):
    """
    holds all error messages
    """

    # general:
    INPUT_NONE = "The given input is None"
    INVALID_TYPE = "The input has got an invalid type"
    INVALID_COLUMN_FILTER = "The column does not fit the filter type"

    # database
    DATABASE_CONNECTION_IMPOSSIBLE = "The connection to the database is not possible"
    DATASET_NOT_EXISTING = "There is no dataset with this idea"
    DATASET_NOT_DELETED = "Error occured while deleting a dataset"
    TRAJECTORY_NOT_EXISTING = "There is no trajectory with this id"
    DATASET_NAME_INVALID = "The name of the dataset is invalid"

    # file:
    ANALYSIS_PATH_NOT_EXISTING = "The standard analysis path does not exist"
    DICT_PATH_NOT_EXISTING = "The standard dictionary path does not exist"
    EXPORT_ERROR = "The export was not successful"
    IMPORT_ERROR = "The import was not successful"
    DATASET_NOT_IMPORTABLE = "The dataset is not convertable (i.e. is contains unrepairable corruptions)"
    DICT_NOT_IMPORTABLE = "The dictionary is not convertable"
    DATASET_CORRUPTED = "The dataset contains corruptions. However, they can be repaired"
    SESSION_NOT_OPEN = "The session is not open"

    # polygons:
    POLYGON_NOT_CREATED_FROM_RECORD = "The polygon could not be created from the record"
    POLYGON_NOT_EXISTING = "The searched polygon does not exist"
    POLYGON_TOO_FEW_POINTS = "A polygon must consist of at least three points."
    POLYGON_ILLEGAL_COORDINATES = "At least one of the selected points does not represent a valid coordinate."
    INVALID_NAME = "The selected name is invalid."
    NOT_ENOUGH_POLYGONS = "There are not enough polygons on the map for this action."
    POLYGON_IN_USE = "Polygon is used in other structures (i.e. filter structure)"
    NO_POLYGON_DELETED = "No polygon was deleted previously"
    NO_POLYGON_ADDED = "No polygon was added previously"

    # filter:
    NO_ABOVE_FILTER_GROUP = "Adding filter group was unsuccessful! The above group does not exist!"
    NOT_ADDABLE_COMPONONENT = "Adding filter group was unsuccessful! The filtergroup can't be added to the component!"
    NO_ADDABLE_COMPONENT = "Reading was unsuccessful! There is no filter yet!"
    FILTER_NOT_ADDED = "Adding filter was unsuccessful!"
    FILTER_NOT_DELETED = "Deleting filter was unsuccessful!"
    RECONSTRUCTION_NOT_POSSIBLE = "Reconstructing filter component was unsuccessful! The component doesn't exist!"
    FILTER_NOT_EXISTING = "The filter does not exist."
    FILTER_GROUP_NOT_EXISTING = "The filter group does not exist."

    # Settings
    SEGMENT_NOT_ADDED = "Adding the segment was unsucessful, " \
                        "because either the location was not found or it already exists"
    PAGE_NOT_ADDED = "Adding the page was unsucessful" \
                     "because either the location was not found or it already exists"
    SETTING_NOT_ADDED = "Adding the page was unsucessful" \
                        "because either the location was not found or it already exists"
    SETTING_NOT_MATCHING = "Updating the setting was unsucessful, because setting structure changed"

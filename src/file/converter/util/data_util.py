import math
import re
from typing import List
from typing import Union

import numpy as np
import pandas as pd
from pandas import Series

CON_VAL: str = "Concrete value"
LW_VAL: str = "Lower available value"
UP_VAL: str = "Upper available value"

UNKNOWN: str = "Unknown"
GENERIC_REGEX: re.Pattern = re.compile('.*')


# Reparations
def repair_number_column(column_frame: pd.DataFrame, def_value: Union[int, float],
                         con_val: str = CON_VAL, linear_transition: bool = False) -> pd.DataFrame:
    """
    repairs a column containing numbers: deletes all non-numeric values with NaN, interpolates and fills empty entries
    :param column_frame:      the column
    :param def_value:         default value
    :param con_val:           the column name (concrete value)
    :param linear_transition: if interpolation is wished
    """
    temporary_frame: pd.DataFrame = pd.DataFrame()
    temporary_frame[con_val] = replace_non_numeric_with_nan(column_frame)
    if linear_transition:
        temporary_frame[con_val] = temporary_frame[con_val].interpolate()

    if check_if_all_nan(temporary_frame[con_val]):
        temporary_frame[con_val].fillna(value=def_value, inplace=True)
        return temporary_frame[con_val]

    temporary_frame[LW_VAL] = temporary_frame[con_val].fillna(method="ffill")
    temporary_frame[UP_VAL] = temporary_frame[con_val].fillna(method="bfill")

    temporary_frame[con_val] = np.where(temporary_frame[con_val].isna(),
                                        (temporary_frame[LW_VAL] + temporary_frame[UP_VAL]) / 2,
                                        temporary_frame[con_val])

    temporary_frame[con_val] = np.where(temporary_frame[con_val].isna(),
                                        temporary_frame[LW_VAL].fillna(temporary_frame[UP_VAL]),
                                        temporary_frame[con_val])

    return temporary_frame[con_val]


def repair_date_column(column_frame: pd.DataFrame, def_value: np.datetime64) -> pd.DataFrame:
    """
    repairs a column containing dates
    :param column_frame:    the column
    :param def_value:       the default value
    """
    temporary_frame: pd.DataFrame = pd.DataFrame()
    temporary_frame[CON_VAL] = replace_non_dates_with_nan(column_frame)

    if check_if_all_nan(temporary_frame[CON_VAL]):
        temporary_frame[CON_VAL].fillna(value=def_value, inplace=True)
        return temporary_frame[CON_VAL]

    temporary_frame[LW_VAL] = temporary_frame[CON_VAL].fillna(method="ffill")
    temporary_frame[UP_VAL] = temporary_frame[CON_VAL].fillna(method="bfill")

    mask = temporary_frame[CON_VAL].isna() & ~temporary_frame[[LW_VAL, UP_VAL]].isna().any(axis=1)
    temporary_frame.loc[mask, CON_VAL] = np.mean(temporary_frame.loc[mask, [LW_VAL, UP_VAL]], axis=1)

    temporary_frame[CON_VAL] = np.where(temporary_frame[CON_VAL].isna(),
                                        temporary_frame[LW_VAL].fillna(temporary_frame[UP_VAL]),
                                        temporary_frame[CON_VAL])

    temporary_frame[CON_VAL] = np.where(temporary_frame[UP_VAL].isna() & temporary_frame[LW_VAL].notna() &
                                        temporary_frame[UP_VAL].isna(),
                                        temporary_frame[LW_VAL],
                                        temporary_frame[UP_VAL])
    temporary_frame[CON_VAL] = np.where(temporary_frame[CON_VAL].isna() & temporary_frame[UP_VAL].notna() &
                                        temporary_frame[LW_VAL].isna(),
                                        temporary_frame[UP_VAL],
                                        temporary_frame[UP_VAL])

    return temporary_frame[CON_VAL]


def repair_string_column(column_frame: pd.DataFrame, regex: re.Pattern = GENERIC_REGEX, def_value: str = UNKNOWN):
    """
    repairs a column containing strings
    :param column_frame:    the column
    :param regex:           the regex that every entry should match
    :param def_value:       the default value
    """
    column_frame = column_frame.applymap(lambda x: np.nan if isinstance(x, str) and x == '' else x)

    column_frame = column_frame.applymap(lambda x: np.nan if isinstance(x, str) and not re.match(regex, x) else x)

    column_frame = column_frame.ffill()

    column_frame = column_frame.bfill()

    column_frame = column_frame.fillna(def_value)

    return column_frame


def delete_duplicate_columns(df, columns):
    """
    deletes duplicate columns
    :param df:      the data frame
    :param columns: the inspected columns
    :return:        the modified dataframe
    """
    duplicate_columns = df.columns[df[columns].duplicated()]
    df = df.drop(duplicate_columns, axis=1)
    return df


def replace_non_numeric_with_nan(df):
    """
    replaces non-numeric values with NaN
    :param df:  the data frame
    :return:    the modified data frame
    """
    df = df.apply(pd.to_numeric, errors='coerce')
    return df


def replace_non_dates_with_nan(df):
    """
    replaces invalid dates with NaN
    :param df:  the data frame
    :return:    the modified data frame
    """
    df = df.apply(lambda x: pd.to_datetime(x, errors='coerce'))
    return df


def check_if_all_nan(df: pd.DataFrame) -> bool:
    """
    checks if all entries are NaN
    :param df:  the data frame
    :return:    whether all entries are NaN
    """
    # DataFrame that masks all entries were NaN is entered to True
    nan_mask = pd.isna(df)

    # Checks if all values are True
    if nan_mask.all().all():
        return True
    return False


# valid checking
def find_duplicate_rows(df: pd.DataFrame, columns: List) -> List:
    """
    Finds duplicate rows in a DataFrame based on the given columns.
    :param df: The DataFrame to search for duplicates.
    :param columns: The columns to use as keys for identifying duplicates.
    :return: A list of all the duplicate rows based on the given columns.
    """
    duplicate_rows = df[df.duplicated(subset=columns, keep=False)].index.to_list()
    return duplicate_rows


def print_duplicate_rows(df: pd.DataFrame, columns: List) -> List[str]:
    """
    Finds duplicate rows in a DataFrame based on the given columns.
    :param df: The DataFrame to search for duplicates.
    :param columns: The columns to use as keys for identifying duplicates.
    :return: A list of all the duplicate rows based on the given columns.
    """
    duplicate_rows = df[df.duplicated(subset=columns, keep=False)].index.to_list()
    if len(duplicate_rows) == 0:
        return []
    return ["at indexes " + str(duplicate_rows)]


def find_non_matching_rows(column_frame: pd.DataFrame, regex: re.Pattern = GENERIC_REGEX) -> List:
    """
    finds all rows that dont match the regex or are no strings
    :param column_frame:    the column
    :param regex:           the regex
    :return:                all rows that dont match
    """
    # Mask for non strings
    non_string_mask = pd.isnull(column_frame) | ~column_frame.apply(lambda x: isinstance(x, str))
    # Mask for non matching
    non_matching_mask = column_frame.apply(lambda x: not pd.isna(x) and not bool(re.match(regex, x)))
    # Combine masks
    mask = non_string_mask | non_matching_mask

    return column_frame[mask]


def print_non_matching_rows(column_frame: pd.DataFrame, regex: re.Pattern = GENERIC_REGEX) -> List:
    """
    finds all rows that dont match the regex or are no strings
    :param column_frame:    the column
    :param regex:           the regex
    :return:                all rows that dont match
    """
    # Mask for non strings
    non_string_mask = pd.isnull(column_frame) | ~column_frame.apply(lambda x: isinstance(x, str))
    # Mask for non matching
    non_matching_mask = column_frame.apply(lambda x: not pd.isna(x) and not bool(re.match(regex, x)))
    # Combine masks
    mask = non_string_mask | non_matching_mask

    non_matching = column_frame[mask]
    if len(non_matching) == 0:
        return []
    return ["Columns " + str(column_frame.columns) + " at indexes " + str(non_matching)]


def find_non_numeric_rows(df: pd.DataFrame) -> List[int]:
    """
    finds all non-numeric rows
    :param df:  the data frame
    :return:    the list of row indices that are non-numeric
    """
    non_numeric_rows = df[pd.to_numeric(df, errors='coerce').isna()].index.to_list()
    return non_numeric_rows


def print_non_numeric_rows(df: pd.DataFrame) -> List[str]:
    """
    finds all non-numeric rows
    :param df:  the data frame
    :return:    the list of row indices that are non-numeric
    """
    non_numeric_rows = df[pd.to_numeric(df, errors='coerce').isna()].index.to_list()
    if len(non_numeric_rows) == 0:
        return []
    return ["Column " + str(df.name) + " at indexes " + str(non_numeric_rows)]


def print_non_date_rows(df: Series) -> List[str]:
    """
    finds all invalid date rows
    :param df:  the data frame
    :return:    the list of row indices that are no valid dates
    """
    non_date_rows = df[pd.to_datetime(df, errors='coerce').isna()].index.to_list()
    if len(non_date_rows) == 0:
        return []
    return ["Column " + str(df.name) + " at indexes " + str(non_date_rows)]


def find_non_date_rows(df: Series) -> List:
    """
    finds all invalid date rows
    :param df:  the data frame
    :return:    the list of row indices that are no valid dates
    """
    non_date_rows = df[pd.to_datetime(df, errors='coerce').isna()].index.to_list()
    return non_date_rows


# Operations and Calculations
def add_distance_to_latitude(latitude, delta_x, delta_y, angle_in_degrees):
    """
    adds a distance to a latitude
    :param latitude:            the latitude
    :param delta_x:                     the delta x coordinate
    :param delta_y:             the delta y coordinate
    :param angle_in_degrees:    the angle
    :return:                    the new latitude
    """
    angle_in_radians = math.radians(angle_in_degrees)

    delta_lat = delta_x * math.cos(angle_in_radians) + delta_y * math.sin(angle_in_radians)
    delta_lat /= 111111

    new_latitude = latitude + delta_lat

    return new_latitude


def add_distance_to_longitude(longitude, latitude, delta_x, delta_y, angle_in_degrees):
    """
    adds a distance to a longitude
    :param longitude:           the longitude
    :param latitude:            the latitude
    :param delta_x:                    the delta x coordinate
    :param delta_y:             the delta y coordinate
    :param angle_in_degrees:    the angle
    :return:                    the new longitude
    """
    angle_in_radians = math.radians(angle_in_degrees)

    delta_lon = -delta_x * math.sin(angle_in_radians) + delta_y * math.cos(angle_in_radians)
    delta_lon /= 111111 * math.cos(math.radians(latitude))

    new_longitude = longitude + delta_lon

    return new_longitude


def calculate_drection(x_column: pd.DataFrame, y_column: pd.DataFrame, head: float) -> pd.DataFrame:
    """
    calculates the direction
    :param x_column:   the x coordinates in a column
    :param y_column:   the y coordinates in a column
    :param head:       the heading
    :return            the dataframe containing the direction
    """
    temporary = np.rad2deg(np.arctan2(y_column, x_column)) + head
    return temporary


class DistanceCalculator:
    """
    calculates the distance
    """

    def __init__(self, lat_col: str, long_col: str):
        self.lat_col = lat_col
        self.long_col = long_col

    def get_distance(self, row: Series):
        """
        Calculates the distance between two coordinates in vectorized form.
        :param  row:    A given row as a series to calculate the distances with.
        :return:        The data containing the distances
        """
        radius_earth = 6378160.0
        lat1 = np.radians(row[self.lat_col])
        long1 = np.radians(row[self.long_col])
        lat2 = np.radians(row[self.lat_col].shift())
        long2 = np.radians(row[self.long_col].shift())

        longitude_difference = np.abs(long2 - long1)
        latitude_difference = np.abs(lat2 - lat1)

        a = np.sin(latitude_difference / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(
            longitude_difference / 2.0) ** 2
        distance = radius_earth * 2 * np.arcsin(np.sqrt(a))
        return distance

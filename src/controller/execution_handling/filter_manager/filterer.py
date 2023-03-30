import colorsys
import uuid
from abc import ABC, abstractmethod
from collections import deque
from random import randint, Random
from typing import List, Optional, Tuple
from uuid import UUID

import numpy as np
import pandas as pd

from src.controller.execution_handling.abstract_manager import AbstractManager
from src.controller.facade_consumer import DataFacadeConsumer
from src.controller.facade_consumer import DatasetFacadeConsumer
from src.controller.facade_consumer import SettingFacadeConsumer
from src.data_transfer.content import Column
from src.data_transfer.content.settings_enum import SettingsEnum
from src.data_transfer.record import DataPointRecord
from src.data_transfer.record import FilterGroupRecord
from src.data_transfer.record import FilterRecord
from src.data_transfer.record import PositionRecord
from src.data_transfer.record import TrajectoryRecord
from src.model.setting_structure.setting_type import Color

# The color internally is stored as HSV, but the user interface uses RGB
MIN_COLOR = 0
MAX_PARAM_COLOR = 180
DEF_COLOR = 230
DEF_PARAM_COLOR = 120
MAX_POSSIBLE_COLOR = 360
HSL_VALUE = 1
HSL_SATURATION = 1
HSL_GREYED_VALUE = 0.2
HSL_GREYED_SATURATION = 0.8
RGB_MAX = 255
COLOR_COL: str = "color"
POS_COL: str = "position"
DREC_COL: str = "data_record"
VISIBLE: str = "visible"


class IFilterer:
    """
    This interface provides the access to the current filtered trajectories.
    """

    @abstractmethod
    def get_filtered_trajectories(self) -> [TrajectoryRecord]:
        """
        Gets all trajectories that pass all filters from the model layer

        :return: The list of trajectories
        """

        pass


class IFilterGetter(ABC):
    """
    This interface is used to get data from the filter structure.
    """

    @abstractmethod
    def get_filter_record(self, filter_id: UUID) -> Optional[FilterRecord]:
        """
        gets the record of the filter with the given id
        :param filter_id:   the id of the filter
        :return:            the filter record
        """
        pass

    @abstractmethod
    def get_filter_group_record(self, group_id: UUID) -> Optional[FilterGroupRecord]:
        """
        gets the record of the filter group with the given id
        :param group_id:    the id of the group
        :return:            the filter group record
        """
        pass

    @abstractmethod
    def get_filter_selections(self, filter_type: str) -> Optional[FilterRecord]:
        """
        gets a standard filter containing the possible selections to create a new filter
        :param filter_type:    the type of the filter
        :return:        a standard filter record
        """
        pass

    @abstractmethod
    def get_filter_group_selection(self) -> Optional[FilterGroupRecord]:
        """
        gets a standard filter group containing the possible selections to create a new filter group
        :return:        a standard filter group record
        """
        pass

    @abstractmethod
    def get_filter_types(self) -> List[str]:
        """
        gets all available types of filter
        :return:    all available types of filter
        """
        pass

    @abstractmethod
    def get_point_filters_root(self) -> Optional[UUID]:
        """
        gets the uuid of the root group of the point filters
        :return: the uuid of the root group of the point filters
        """
        pass

    @abstractmethod
    def get_trajectory_filters_root(self) -> Optional[UUID]:
        """
        gets th uuid of the root group of the trajectory filters
        :return: the root group of the trajectory filters
        """
        pass


class Filterer(IFilterer, DataFacadeConsumer, DatasetFacadeConsumer, SettingFacadeConsumer, AbstractManager):
    """
    This class implements the Filterer. The Filterer is the core component to translate the tabular databse trajectory
    data to the graphical representation. It is responsible for the filtering of the data and the calculation of the
    colors of the trajectories.
    """

    def __init__(self):
        IFilterer.__init__(self)
        DataFacadeConsumer.__init__(self)
        DatasetFacadeConsumer.__init__(self)
        SettingFacadeConsumer.__init__(self)
        AbstractManager.__init__(self)
        self._color_map: dict = {Color.UNI: self.calculate_uni, Color.RANDOM: self.calculate_random,
                                 Color.PARAMETER: self.calculate_param}
        self.color_calc: callable = self.calculate_uni

        self.old_color_type: Color = Color.UNI

        self.old_seed: int = 0
        self.old_random: bool = False
        self.old_offset: int = 0
        self.greyed_out: bool = False

        self.all_data_points: pd.DataFrame = None
        self.old_trajectories = list()
        self.current_trajectories = list()

        self.current_data = None
        self.old_data = None

    def get_filtered_trajectories(self) -> [TrajectoryRecord]:
        """
        Gets all trajectories that pass all filters from the model layer.
        It calculates only the displayed trajectories, not all trajectories.
        It also calculates the colors of the trajectories and the positions of the data points.
        :return: The list of trajectories
        """
        self.greyed_out = self.setting_facade.get_settings_record().find(SettingsEnum.FILTER_GREYED)[0].selected[0]
        if not self.calculate_trajectories():
            return []
        if not self.select_color():
            return []
        return self.calculate_records()

    def load_data(self, additional_columns: List[Column] = None) -> bool:
        """
        This method loads the concrete data (ids, latitudes, longitudes, times, order) from the database. It only
        loads the trajectories that are currently displayed.
        """
        columns_to_load: List[Column] = [Column.ID, Column.TRAJECTORY_ID, Column.LATITUDE, Column.LONGITUDE,
                                         Column.TIME, Column.ORDER]

        if additional_columns is not None:
            for additional_column in additional_columns:
                if additional_column not in columns_to_load:
                    columns_to_load.append(additional_column)

        self.old_data = self.current_data

        data = self.data_facade.get_data_of_column_selection(
            columns_to_load,
            self.current_trajectories,
            Column.TRAJECTORY_ID, usefilter=False)

        if data is None:
            self.handle_error([self._data_facade, self._dataset_facade])
            return False

        self.current_data = data.data
        self.current_data[VISIBLE] = self.current_data[Column.ID.value].isin(self.all_data_points[Column.ID.value])

        self.current_data[Column.ID.value] = self.current_data[Column.ID.value].apply(lambda x: uuid.UUID(x))
        self.current_data[Column.TRAJECTORY_ID.value] = \
            self.current_data[Column.TRAJECTORY_ID.value].apply(lambda x: uuid.UUID(x))

        # Create a column POS_COL with PositionRecords. The position records are created from the lat and long columns.
        # The method does not use pandas dataframe methods instead of a for loop, because they are more efficient
        def create_position_record(row):
            return PositionRecord(_longitude=row[Column.LONGITUDE.value], _latitude=row[Column.LATITUDE.value])

        # Apply the function to create a new column 'PositionRecord'
        self.current_data[POS_COL] = self.current_data.apply(create_position_record, axis=1)

        return True

    def calculate_records(self):
        """
        Calculates the TrajectoryRecords from the current data.
        :return: The list of TrajectoryRecords
        """
        self.current_data[DREC_COL] = self.current_data.apply(lambda row:
                                                              DataPointRecord(_uuid=row[Column.ID.value],
                                                                              _filtered=row[VISIBLE],
                                                                              _position=row[POS_COL],
                                                                              _visualisation=row[COLOR_COL]), axis=1)

        step_size: int = self.setting_facade.get_settings_record().find(SettingsEnum.TRAJECTORY_STEP_SIZE)[0].selected[
            0]

        # define function to create a tuple of datapoint records and the trajectory id for each Trajectory group
        def create_trajectory_record(group_original_index, step):
            """
            internal function to create a TrajectoryRecord from a group. part of the dataframe corresponding to a
            trajectory.
            :param group_original_index:
            :param step:
            :return:
            """
            if not self.greyed_out:
                group_original_index = group_original_index[group_original_index[VISIBLE]]
            # sort the original index of the group by time, because the original index is not sorted.

            group = group_original_index.sort_values(Column.ORDER.value).reset_index().drop("index", axis=1)
            trajectory_id = group[Column.TRAJECTORY_ID.value].iloc[0]

            # always include first datapoint record
            datapoint_records: List[DataPointRecord] = [group[DREC_COL].iloc[0]]

            # select every step'th datapoint record in the group (excluding first and last datapoint record)
            filter_string = f'index > 0 and index < {len(group) - 1} and (index - 1) % {step} == 0'
            selected_records = group.query(filter_string)[DREC_COL].tolist()
            datapoint_records.extend(selected_records)

            # always include last datapoint record
            datapoint_records.append(group[DREC_COL].iloc[-1])
            return TrajectoryRecord(_id=trajectory_id, _datapoints=tuple(datapoint_records))

        # group dataframe by Trajectory column, and apply create_trajectory_record function to create a tuple of
        # datapoint records and the trajectory id for each group
        trajectories = self.current_data.groupby(Column.TRAJECTORY_ID.value).apply(create_trajectory_record,
                                                                                   step=step_size).tolist()
        return trajectories

    def select_color(self) -> bool:
        """
        Gets the current selected color and calls the corresponding method to calculate the colors.
        """
        color_type = self.setting_facade.get_settings_record().find(SettingsEnum.COLOR_SETTINGS)[0].selected[0]
        self.color_calc = self._color_map[color_type]
        return self.color_calc()

    def calculate_random(self) -> bool:
        """
        Calculates random colors for the trajectories.
        Takes over the old colors if the trajectories are the same.
        :return: True if the calculation was successful, False otherwise
        """

        if not self.load_data():
            return False

        if self.old_color_type == Color.RANDOM:
            id_color_dict = dict(self.old_data.drop_duplicates(subset=[Column.TRAJECTORY_ID.value], keep='first')
                                 [[Column.TRAJECTORY_ID.value, COLOR_COL]].values)
        else:
            id_color_dict = dict()
        self.old_color_type = Color.RANDOM

        def generate_random_color(trajec_id, visible: bool):
            if trajec_id not in id_color_dict:
                # Generate a random color if the 'id' does not exist in the dictionary
                color = self.convert_hsv_to_rgb(randint(MIN_COLOR, MAX_POSSIBLE_COLOR), True)
                id_color_dict[trajec_id] = color
            return self.reset_rgb(id_color_dict[trajec_id], visible)

        # assign the color for each row using the id column and color map
        self.current_data[COLOR_COL] = self.current_data.apply(
            lambda row: generate_random_color(row[Column.TRAJECTORY_ID.value],
                                              row[VISIBLE]), axis=1)
        return True

    def calculate_uni(self) -> bool:
        """
        Gives the trajectory a predefined color
        """
        if not self.load_data():
            return False

        self.current_data[COLOR_COL] = self.current_data.apply(lambda row: self.convert_hsv_to_rgb(DEF_COLOR,
                                                                                                   row[VISIBLE]),
                                                               axis=1)
        self.old_color_type = Color.UNI
        return True

    def calculate_param(self) -> bool:
        """
        Calculates the color based on the parameter. The color is calculated by the quotient of the parameter value and
        the maximum parameter value.
        """
        column = self.setting_facade.get_settings_record().find(SettingsEnum.TRAJECTORY_PARAM_COLOR)[0].selected[0]

        if not self.load_data([column]):
            return False

        self.current_data[COLOR_COL] = self.current_data.apply(lambda row: self.convert_hsv_to_rgb(DEF_COLOR,
                                                                                                   row[VISIBLE]),
                                                               axis=1)
        min_occur = self.current_data[column.value].min()
        max_occur = self.current_data[column.value].max()

        if min_occur == max_occur:
            self.current_data[COLOR_COL] = self.current_data.apply(lambda row: self.convert_hsv_to_rgb(DEF_PARAM_COLOR,
                                                                                                       row[VISIBLE]),
                                                                   axis=1)
            return True
        min_max_quotient = 1 / (max_occur - min_occur)
        self.current_data[COLOR_COL] = self.current_data.apply(lambda row: self.convert_hsv_to_rgb(
            (row[column.value] - min_occur) * min_max_quotient *
            ((MAX_PARAM_COLOR - MIN_COLOR) + MIN_COLOR), row[VISIBLE]), axis=1)
        self.old_color_type = Color.PARAMETER

        return True

    def calculate_trajectories(self) -> bool:
        """
        Calculates the displayed trajectories.
        Firstly calls the method to get visible trajectories.
        Then it calculates the offset and the length of the displayed trajectory list.
        Then rotates the trajectory list by the offset.
        Saves the old trajectory list.

        By default it returns the first n trajectories, where n is the sample size, from the previous trajectory list to
        counter filter changes. Only if the settings change, completely new trajectories are calculated.
        """

        trajectory_list = self.get_visible_trajectories()
        if trajectory_list is None:
            return False

        trajectory_list.sort()

        offset_ratio: float = self.setting_facade.get_settings_record().find(SettingsEnum.OFFSET)[0].selected[0]
        random: bool = self.setting_facade.get_settings_record().find(SettingsEnum.RANDOM_SAMPLE)[0].selected[0]
        seed: int = self.setting_facade.get_settings_record().find(SettingsEnum.RANDOM_SEED)[0].selected[0]

        offset = int(len(trajectory_list) * offset_ratio)
        length: int = self.setting_facade.get_settings_record().find(SettingsEnum.TRAJECTORY_SAMPLE_SIZE)[0].selected[0]
        if len(trajectory_list) <= length:
            length = len(trajectory_list)
        length = int(length)

        test_list = deque(trajectory_list)
        test_list.rotate(offset)
        trajectory_list = list(test_list)

        self.old_trajectories = self.current_trajectories
        self.current_trajectories = list()

        if random:
            Random(seed).shuffle(trajectory_list)
            if seed != self.old_seed or not self.old_random:
                self.current_trajectories = trajectory_list[:length]
                return True

        if not random:
            if self.old_random:
                self.current_trajectories = trajectory_list[:length]
                return True

        if self.old_offset != offset:
            self.current_trajectories = trajectory_list[:length]
            self.old_offset = offset
            return True

        for entry in self.old_trajectories:
            if entry in trajectory_list and len(self.current_trajectories) < length:
                self.current_trajectories.append(entry)

        # If the desired length is not reached yet, add entries from list2 that are not already in list3
        for entry in trajectory_list:
            if entry not in self.current_trajectories and len(self.current_trajectories) < length:
                self.current_trajectories.append(entry)
            if len(self.current_trajectories) == length:
                break

        return True

    def get_visible_trajectories(self) -> Optional[List[uuid.UUID]]:
        """
        Gets all trajectories which contain at least one visible data point.
        """
        data = self.data_facade.get_data([Column.TRAJECTORY_ID, Column.ID])
        if data is None:
            self.handle_error([self._data_facade, self._dataset_facade])
            return None
        self.all_data_points = data.data

        data_point_trajectories = data.data[Column.TRAJECTORY_ID.value].unique()
        trajectories = self.data_facade.get_trajectory_ids()

        if trajectories is None:
            self.handle_error([self._data_facade, self._dataset_facade])
            return None

        trajectories = trajectories.data[Column.TRAJECTORY_ID.value]
        joined_trajectories = np.intersect1d(trajectories, data_point_trajectories)

        return [uuid.UUID(x) for x in joined_trajectories]

    def reset_rgb(self, rgb: int, visible: bool) -> int:
        """
        Resets the HSV color to the default color
        """

        r = (rgb >> 16) & 0xFF
        g = (rgb >> 8) & 0xFF
        b = rgb & 0xFF

        # Convert RGB to HSV
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        h = int(h * MAX_POSSIBLE_COLOR)
        return self.convert_hsv_to_rgb(h, visible)

    def convert_hsv_to_rgb(self, hsv_color: int, visible: bool) -> int:
        """
        Converts a HSV color to RGB
        """
        if not visible:
            rgb_color_tuple: Tuple[float, float, float] = colorsys.hsv_to_rgb(hsv_color / MAX_POSSIBLE_COLOR,
                                                                              HSL_GREYED_VALUE, HSL_GREYED_SATURATION)
        else:
            rgb_color_tuple: Tuple[float, float, float] = colorsys.hsv_to_rgb(hsv_color / MAX_POSSIBLE_COLOR,
                                                                              HSL_VALUE, HSL_SATURATION)
        # Convert to rgb color value int
        return (int(rgb_color_tuple[0] * RGB_MAX) << 16) + (int(rgb_color_tuple[1] * RGB_MAX) << 8) \
            + int(rgb_color_tuple[2] * RGB_MAX)

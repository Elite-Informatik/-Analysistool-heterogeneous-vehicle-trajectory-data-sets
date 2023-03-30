from abc import ABC
from typing import Optional

import numpy as np
import pandas as pd
from pandas import Series
from shapely.geometry import Point
from shapely.geometry import Polygon

from src.data_transfer.content import Column
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import PolygonRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.model.analysis_structure.Analysis import Analysis
from src.model.analysis_structure.spatial_analysis.polygon_consumer_analysis import PolygonFacadeConsumer
from src.model.polygon_structure.ipolygon_structure import IPolygonStructure


def point_in_polygon(lat: float, long: float, polygon_record: PolygonRecord):
    """
    Checks if a given point is inside a polygon. It does not account for the curvature of the earth.
    :param lat: the latitude as a float of the point
    :param long: the longitude of the point
    :param polygon_record: the polygon that might contain the point
    :return: True if the point is the record and false
    """
    polygon = Polygon([Point(corner.to_tuple()) for corner in polygon_record.corners])
    return polygon.contains(Point(lat, long))


def get_distance(row: Series):
    """
    Calculates the distance between two coordinates in vectorized form.
    :param row: The Series of a group derived from the trajectory id group.
    :return: The data containing the distances
    """
    radius_earth = 6378160.0
    lat1 = np.radians(row[Column.LATITUDE.value])
    long1 = np.radians(row[Column.LONGITUDE.value])
    lat2 = np.radians(row[Column.LATITUDE.value].shift())
    long2 = np.radians(row[Column.LONGITUDE.value].shift())

    longitude_difference = np.abs(long2 - long1)
    latitude_difference = np.abs(lat2 - lat1)

    a = np.sin(latitude_difference / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(longitude_difference / 2.0) ** 2
    distance = radius_earth * 2 * np.arcsin(np.sqrt(a))

    return distance


class StartEndAnalysis(Analysis, PolygonFacadeConsumer, ABC):
    """
    An abstract class for any analysis that requires a start and an end polygon. It has the capabilities to prepare the
    data for later analysis by adding the distance driven as well as the time taken by a trajectory to the data.
    """
    _columns = [Column.TRAJECTORY_ID.value, Column.DATE.value, Column.TIME.value, Column.LONGITUDE.value,
                Column.LATITUDE.value]

    def __init__(self, name: str):
        """
        Initializes the class with default parameters
        """
        super().__init__()
        self._required_parameters = self._columns
        self._start_polygon = None
        self._end_polygon = None
        self.__current_record: Optional[AnalysisRecord] = None
        self._name: str = name

    @property
    def _current_record(self) -> AnalysisRecord:
        """
        An internal property to check if the record is set before accessing it. This way it avoids if statements
        checking against None anytime the parameter is attempted to be accessed.
        :return: The default record if set.
        """
        if self.__current_record is None:
            raise RuntimeError("The analysis is in an illegal state. The _default_record attribute was attempted to be"
                               "accessed before it was set.")
        return self.__current_record

    def set_polygon_structure(self, structure: IPolygonStructure) -> None:
        """
        Sets the polygon structure in order for the analysis to access the possible polygons.
        :param structure: The polygon structure.
        """
        polygons = structure.get_all_polygons()

        if len(polygons) == 0:
            raise ValueError("No Polygons are selectable.")

        if len(polygons) == 1:
            polygons = [polygons[0], polygons[0]]

        self.set_analysis_parameters(
            AnalysisRecord(
                _required_data=(
                    SettingRecord(
                        _context="start and end polygon",
                        _selection=SelectionRecord(
                            selected=polygons[0:2],
                            option=DiscreteOption(polygons),
                            possible_selection_range=range(2, 3)
                        )
                    ),
                ),
            )
        )

    def get_required_analysis_parameter(self) -> AnalysisRecord:
        """
        Returns the default record of the analysis to be set by the user.
        :return: default record of the analysis
        """
        return self._current_record

    def get_name(self) -> str:
        """
        Returns the _name of the analysis
        :return: _name of the analysis
        """
        return self._name

    def set_analysis_parameters(self, record: AnalysisRecord) -> bool:
        """
        Set the analysis parameters with the passed record
        :param record: record with analysis parameters
        :return: True if the record is valid and parameters are set
        """
        if len(record.required_data) != 1:
            raise ValueError("The record does not contain the correct number of option.")
        option = record.required_data[0].selection.option
        selected_polygons = record.required_data[0].selection.selected
        if len(selected_polygons) != 2 or not all(option.is_valid(polygon) for polygon in selected_polygons):
            raise ValueError("Two valid polygon attribute needs to be selected for the path time analysis.")

        self._start_polygon, self._end_polygon = record.required_data[0].selection.selected[0], \
            record.required_data[0].selection.selected[1]
        self.__current_record = record
        return True

    def _get_distance_time(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Analyzes the data by calculating time taken for a given distance.
        :param data: data to be analyzed
        :return: result of the analysis as an pandas Dataframe
        """

        ns_to_seconds = 1000000000
        data_df = data[self._columns]
        # Create the polygon_id data containing the order in which the polygons were passed through.
        polygon_calculator = self.PolygonCalculator(self._start_polygon, self._end_polygon)
        data_df['polygon_id'] = data_df.apply(polygon_calculator.get_polygon_row, axis=1)
        data_df['polygon_id'] = data_df.groupby(Column.TRAJECTORY_ID.value)['polygon_id'].diff().fillna(0)

        # Calculates the time delta between points on a trajectory.
        data_df['time'] = pd.to_datetime(data_df[Column.DATE.value] + ' ' + data_df[Column.TIME.value],
                                         format='%d.%m.%Y %H:%M:%S')
        data_df['time'] = pd.to_numeric(data_df['time'] - data_df.groupby(Column.TRAJECTORY_ID.value)['time']
                                        .transform('first')) / ns_to_seconds

        # Calculates the distance between two points in the data and rounds it to two decimal places.
        data_df['distance'] = data_df.groupby(Column.TRAJECTORY_ID.value).apply(get_distance).reset_index().iloc[:, -1:]
        data_df['distance'] = data_df.groupby(Column.TRAJECTORY_ID.value)['distance'].cumsum().fillna(0).round(2)

        # filter out all the trajectories which do not go from the start to the end polygon.
        data_df = data_df.groupby(Column.TRAJECTORY_ID.value).filter(lambda x: 1 in x['polygon_id'].unique()) \
            .reset_index()

        return data_df

    class PolygonCalculator:
        """
        A class responsible for calculating which of the given start and end polygon a point is in. If a point is in
        no polygon the last polygon is given.
        """

        def __init__(self, start_polygon, end_polygon):
            """
            A constructor for setting the required parameters.
            :param start_polygon: the start polygon
            :param end_polygon: the end polygon.
            """
            self.last_trajectory = 0
            self.last_polygon = 0
            self._start_polygon = start_polygon
            self._end_polygon = end_polygon

        def get_polygon_row(self, row: Series) -> int:
            """
            The method that calculates the polygon.
            :param row: A data of a dataframe as a series.
            :return: The polygon in which the point lies or the last set polygon.
            """
            long: float = row[Column.LONGITUDE.value]
            lat: float = row[Column.LATITUDE.value]
            if row[Column.TRAJECTORY_ID.value] != self.last_trajectory:
                self.last_trajectory = row[Column.TRAJECTORY_ID.value]
                self.last_polygon = 0
            for polygon_id, polygon in enumerate([self._start_polygon, self._end_polygon]):
                if point_in_polygon(lat, long, polygon):
                    self.last_polygon = polygon_id + 1
                    return polygon_id + 1
            return self.last_polygon

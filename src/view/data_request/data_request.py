import time
from typing import List
from uuid import UUID

from src.controller.input_handling.request_distributor import RequestDistributor
from src.data_transfer.content.column import Column
from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import AnalysisTypeRecord
from src.data_transfer.record import DataRecord
from src.data_transfer.record import DatasetRecord
from src.data_transfer.record import FilterGroupRecord
from src.data_transfer.record import FilterRecord
from src.data_transfer.record import PolygonRecord
from src.data_transfer.record import SettingsRecord
from src.data_transfer.record import TrajectoryRecord
from src.data_transfer.record.setting_record import SettingRecord


class DataRequest:
    """
    This Class is a proxy for the data request facade of the controller. It provides functionalities that
    allow the user interface elements to get the data they want to show.
    """

    def __init__(self, data_request: RequestDistributor):
        """
        Creates a new DataRequest instance. All user interface elements use the same instance to query their data.

        :param data_request: Controller interface which provides functions to request data from the controller
        """
        self._data_request: RequestDistributor = data_request

    def get_dataset_meta(self, dataset_id: UUID) -> DatasetRecord:
        """
        returns a specific dataset record which holds the metadata of the dataset

        :param dataset_id: id of the dataset
        """
        return self._data_request.get_dataset_meta(dataset=dataset_id)

    def get_rawdata(self, selected_column: List[Column]) -> DataRecord:
        """
        Gets specific columns of the datasets independent on the trajectories

        :param selected_column: the columns type to return

        :return: The data record
        """
        return self._data_request.get_rawdata(selected_column)

    def get_polygon_ids(self) -> List[UUID]:
        """
        returns a list of all polygon ids
        """
        return self._data_request.get_polygon_ids()

    def get_polygon(self, id: UUID) -> PolygonRecord:
        """
        returns the polygon data of a specific polygon

        :param id: id of the polygon
        """
        return self._data_request.get_polygon(id)

    def get_analysis_types(self) -> List[AnalysisTypeRecord]:
        """
        gets all available types of analyses
        :return: all available types of analyses
        """
        return self._data_request.get_analysis_types()

    def get_analysis_data(self, analysis_id: UUID) -> AnalysisDataRecord:
        """
        gets the analyzed data of an analysis
        :param analysis_id:     the id of the analysis
        :return:                the analyzed data
        """
        return self._data_request.get_analysis_data(analysis_id)

    def get_analysis_settings(self, uuid: UUID) -> AnalysisRecord:
        """
        gets the required data of an analysis type
        :param uuid:    the type of the analysis
        :return:        the required data
        """
        return self._data_request.get_analysis_settings(uuid)

    def get_settings(self) -> SettingsRecord:
        """
        returns the current selected settings together with all possible
        selections.
        """
        return self._data_request.get_settings()

    def get_root_datapoint_filter(self) -> UUID:
        """
        returns the uuid of the root filter group of the datapoint filters
        """
        return self._data_request.get_point_filters_root()

    def get_root_trajectory_filter(self) -> UUID:
        """
        returns the uuid of the root filter group of the trajectory filters
        """
        return self._data_request.get_trajectory_filters_root()

    def get_filter_group(self, filter_group: UUID) -> FilterGroupRecord:
        """
        returns the Filter Group data for the filter with the given uuid
        """
        return self._data_request.get_filter_group(filter_group)

    def get_shown_trajectories(self) -> List[TrajectoryRecord]:
        """
        returns the trajectories that should be displayed on the map
        """
        start = time.time()
        result = self._data_request.get_shown_trajectories()
        end = time.time()
        print("\n", end - start, "\n")
        return result

    def get_discrete_selection_column(self, column: Column) -> SettingRecord:
        """
        returns a setting that defines a selection for a Value from the given dataset column
        """
        return self._data_request.get_discrete_selection_column(column)

    def get_interval_selection_column(self, column: Column) -> SettingRecord:
        """
        returns a setting that defines a selection for an interval from the given dataset column
        """
        return self._data_request.get_interval_selection_column(column)

    def get_standard_filter(self, filter_type: str) -> FilterRecord:
        """
        returns a record that defines a standard filter record that is used to create the selection
        of a new Filter
        """
        return self._data_request.get_filter_selections(filter_type=filter_type)

    def get_standard_filter_group(self) -> FilterGroupRecord:
        """
        returns the filter group record that contains the standard data for an uninitialized filter group.
        """
        return self._data_request.get_filter_group_selection()

    def get_data_formats(self):
        """
        returns a list with all data formats
        """
        return self._data_request.get_convertable_file_formats()

    def get_filter(self, filter_id: UUID) -> FilterRecord:
        """
        Returns the Filter Record for a filter with the given UUID
        """
        return self._data_request.get_filter(filter_id)

    def get_trajectory_data(self, trajectory_id: UUID):
        """
        returns the data of the trajectory with the given uuid
        """
        return self._data_request.get_rawdata_trajectory(trajectory=trajectory_id)

    def get_datapoint_data(self, datapoint_id: UUID):
        """
        returns the data of the datapoint with the given uuid
        """
        return self._data_request.get_rawdata_datapoint(datapoint=datapoint_id)

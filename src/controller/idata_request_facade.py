from abc import ABC
from abc import abstractmethod
from typing import List
from uuid import UUID

from src.data_transfer.content import Column
from src.data_transfer.content import FilterType
from src.data_transfer.content.logger import logging
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


class IDataRequestFacade(ABC):
    """
    this interface represents the data request facade to request data from the controller
    """

    @logging
    @abstractmethod
    def get_rawdata_trajectory(self, trajectory: UUID) -> DataRecord:
        """
        gets the raw data of the trajectory with the given id
        :param trajectory:  the id of the trajectory
        :return:            the raw data
        """
        pass

    @logging
    @abstractmethod
    def get_rawdata(self, selected_column: [Column]) -> DataRecord:
        """
        Gets specific columns of the datasets independent on the trajectories

        :param selected_column: the columns type to return

        :return: The data record
        """
        pass

    @logging
    @abstractmethod
    def get_rawdata_datapoint(self, datapoint: UUID) -> DataRecord:
        """
        gets the raw data of the datapoint with the given id
        :param datapoint:   the id of the datapoint
        :return:            the raw data
        """
        pass

    @logging
    @abstractmethod
    def get_shown_trajectories(self) -> List[TrajectoryRecord]:
        """
        gets all shown trajectories
        :return: all shown trajectories
        """
        pass

    @logging
    @abstractmethod
    def get_polygon(self, polygon: UUID) -> PolygonRecord:
        """
        gets the polygon record of the polygon with the given id
        :param polygon:     the id of the polygon
        :return:            the polygon record
        """
        pass

    @logging
    @abstractmethod
    def get_polygon_ids(self) -> List[UUID]:
        """
        gets the ids of all polygons
        :return: all polygon ids
        """
        pass

    @logging
    @abstractmethod
    def get_filter(self, filter_uuid: UUID) -> FilterRecord:
        """
        gets the filter record of the filter with the given id
        :param filter_uuid:  the id of the filter
        :return:        the filter record
        """
        pass

    @logging
    @abstractmethod
    def get_filter_types(self) -> List[FilterType]:
        """
        gets all available types of filter
        :return:    all available types of filter
        """
        pass

    @logging
    @abstractmethod
    def get_filter_selections(self, filter_type: FilterType) -> FilterRecord:
        """
        gets a standard filter containing the possible selections to create a new filter
        :param filter_type:    the type of the filter
        :return:        a standard filter record
        """
        pass

    @logging
    @abstractmethod
    def get_filter_group_selection(self) -> FilterGroupRecord:
        """
        gets a standard filter group containing the possible selections to create a new filter group
        :return:        a standard filter group record
        """
        pass

    @logging
    @abstractmethod
    def get_analysis_types(self) -> List[AnalysisTypeRecord]:
        """
        gets all available types of analyses
        :return: all available types of analyses
        """
        pass

    @logging
    @abstractmethod
    def get_analysis_settings(self, uuid: UUID) -> AnalysisRecord:
        """
        gets the required data of an analysis type
        :param uuid:    the type of the analysis
        :return:        the required data
        """
        pass

    @logging
    @abstractmethod
    def get_analysis_data(self, analysis_id: UUID) -> AnalysisDataRecord:
        """
        gets the analyzed data of an analysis
        :param analysis_id:     the id of the analysis
        :return:                the analyzed data
        """
        pass

    @logging
    @abstractmethod
    def get_settings(self) -> SettingsRecord:
        """
        gets the current settings
        :return: the settings as a record
        """
        pass

    @logging
    @abstractmethod
    def get_dataset_meta(self, dataset: UUID) -> DatasetRecord:
        """
        gets the metadata of the dataset with the given id
        :param dataset:     the id of the dataset
        :return:            the metadata of the dataset
        """
        pass

    @logging
    @abstractmethod
    def get_filter_group(self, filter_group: UUID) -> FilterGroupRecord:
        """
        gets the filter group data for the group with the given id
        """
        pass

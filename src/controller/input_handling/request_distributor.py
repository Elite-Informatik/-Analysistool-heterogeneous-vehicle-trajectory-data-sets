from typing import List
from uuid import UUID

from src.controller.execution_handling.analysis_manager import IAnalysisGetter
from src.controller.execution_handling.database_manager import IDatabaseGetter
from src.controller.execution_handling.filter_manager.filter_manager import IFilterGetter
from src.controller.execution_handling.filter_manager.filterer import IFilterer
from src.controller.execution_handling.polygon_manager import IPolygonGetter
from src.controller.execution_handling.setting_manager import ISettingGetter
from src.controller.facade_consumer import FileFacadeConsumer
from src.controller.idata_request_facade import IDataRequestFacade
from src.data_transfer.content import Column
from src.data_transfer.content.logger import logging
from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import AnalysisTypeRecord
from src.data_transfer.record import DataRecord
from src.data_transfer.record import DatasetRecord
from src.data_transfer.record import FilterGroupRecord
from src.data_transfer.record import FilterRecord
from src.data_transfer.record import PolygonRecord
from src.data_transfer.record import SettingRecord
from src.data_transfer.record import SettingsRecord
from src.data_transfer.record import TrajectoryRecord


class RequestDistributor(IDataRequestFacade, FileFacadeConsumer):
    """
    This class represents the data request facade of the controller.
    The view can request current data via this interface.
    """

    def __init__(self, setting_getter: ISettingGetter = None, polygon_getter: IPolygonGetter = None,
                 analysis_getter: IAnalysisGetter = None, filter_getter: IFilterGetter = None,
                 filterer: IFilterer = None, data_getter: IDatabaseGetter = None):
        super().__init__()
        self._setting_getter: ISettingGetter = setting_getter
        self._polygon_getter: IPolygonGetter = polygon_getter
        self._analysis_getter: IAnalysisGetter = analysis_getter
        self._filter_getter: IFilterGetter = filter_getter
        self._filterer: IFilterer = filterer
        self._data_getter: IDatabaseGetter = data_getter

    @logging
    def set_getter(self, setting_getter: ISettingGetter,
                   polygon_getter: IPolygonGetter,
                   data_getter: IDatabaseGetter,
                   filter_getter: IFilterGetter,
                   analysis_getter: IAnalysisGetter,
                   filterer: IFilterer):
        """
        Setter for the different model getter
        """
        self._setting_getter = setting_getter
        self._polygon_getter = polygon_getter
        self._data_getter = data_getter
        self._filter_getter = filter_getter
        self._analysis_getter = analysis_getter
        self._filterer = filterer

    @logging
    def get_rawdata_trajectory(self, trajectory: UUID) -> DataRecord:
        """
        gets the raw data of the trajectory with the given id
        :param trajectory:  the id of the trajectory
        :return:            the raw data
        """
        return self._data_getter.get_rawdata_trajectory(trajectory)

    @logging
    def get_rawdata(self, selected_column: List[Column]) -> DataRecord:
        """
        Gets specific columns of the datasets independent on the trajectories

        :param selected_column: the columns type to return

        :return: The data record
        """
        return self._data_getter.get_rawdata(selected_column)

    @logging
    def get_rawdata_datapoint(self, datapoint: UUID) -> DataRecord:
        """
        gets the raw data of the datapoint with the given id
        :param datapoint:   the id of the datapoint
        :return:            the raw data
        """
        return self._data_getter.get_rawdata_datapoint(datapoint)

    @logging
    def get_shown_trajectories(self) -> List[TrajectoryRecord]:
        """
        gets all shown trajectories
        :return: all shown trajectories
        """
        return self._filterer.get_filtered_trajectories()

    @logging
    def get_polygon(self, polygon: UUID) -> PolygonRecord:
        """
        gets the polygon record of the polygon with the given id
        :param polygon:     the id of the polygon
        :return:            the polygon record
        """
        return self._polygon_getter.get_polygon(polygon)

    @logging
    def get_polygon_ids(self) -> List[UUID]:
        """
        gets the ids of all polygons
        :return: all polygon ids
        """
        return self._polygon_getter.get_polygon_ids()

    @logging
    def get_filter(self, filter_id: UUID) -> FilterRecord:
        """
        gets the filter record of the filter with the given id
        :param filter_id:  the id of the filter
        :return:        the filter record
        """
        return self._filter_getter.get_filter_record(filter_id)

    @logging
    def get_filter_group(self, filter_group: UUID) -> FilterGroupRecord:
        """
        gets the filter group record of the filter group with the given id
        :param filter_group: the id of the filter_group
        :return: the filter group record
        """
        return self._filter_getter.get_filter_group_record(filter_group)

    @logging
    def get_filter_types(self) -> List[str]:
        """
        gets all available types of filter
        :return:    all available types of filter
        """
        return self._filter_getter.get_filter_types()

    @logging
    def get_filter_selections(self, filter_type: str) -> FilterRecord:
        """
        gets a standard filter containing the possible selections to create a new filter
        :param filter_type:    the type of the filter
        :return:        a standard filter record
        """
        return self._filter_getter.get_filter_selections(filter_type)

    @logging
    def get_filter_group_selection(self) -> FilterGroupRecord:
        """
        gets a standard filter group containing the possible selections to create a new filter group
        :return:        a standard filter group record
        """
        return self._filter_getter.get_filter_group_selection()

    @logging
    def get_point_filters_root(self) -> UUID:
        """
        gets the uuid of the root group of the point filters
        :return: the uuid of the root group of the point filters
        """
        return self._filter_getter.get_point_filters_root()

    @logging
    def get_trajectory_filters_root(self) -> UUID:
        """
        gets th uuid of the root group of the trajectory filters
        :return: the root group of the trajectory filters
        """
        return self._filter_getter.get_trajectory_filters_root()

    @logging
    def get_analysis_types(self) -> List[AnalysisTypeRecord]:
        """
        gets all available types of analyses
        :return: all available types of analyses
        """
        return self._analysis_getter.get_analysis_types()

    @logging
    def get_analysis_settings(self, uuid: UUID) -> AnalysisRecord:
        """
        gets the required data of an analysis type
        :param uuid:    the type of the analysis
        :return:        the required data
        """
        return self._analysis_getter.get_analysis_settings(uuid)

    @logging
    def get_analysis_data(self, analysis_id: UUID) -> AnalysisDataRecord:
        """
        gets the analyzed data of an analysis
        :param analysis_id:     the id of the analysis
        :return:                the analyzed data
        """
        return self._analysis_getter.get_analysis_data(analysis_id)

    @logging
    def get_settings(self) -> SettingsRecord:
        """
        gets the current settings
        :return: the settings as a record
        """
        return self._setting_getter.get_settings_record()

    @logging
    def get_dataset_meta(self, dataset: UUID) -> DatasetRecord:
        """
        gets the metadata of the dataset with the given id
        :param dataset:     the id of the dataset
        :return:            the metadata of the dataset
        """
        return self._data_getter.get_dataset_meta(dataset)

    @logging
    def get_discrete_filterable_columns(self) -> List[Column]:
        """
        Returns all Columns that exist in the current working dataset and which can be filtered with
        a discrete filter.
        """
        return Column.get_discrete_columns()

    @logging
    def get_interval_filterable_columns(self) -> List[Column]:
        """
        Returns all Columns that exist in the current working dataset and which can be filtered with
        a discrete filter.
        """
        return Column.get_interval_columns()

    @logging
    def get_convertable_file_formats(self) -> List[str]:
        """
        Returns the file format that are convertable
        """
        return self._file_facade.convertabele_file_formats

    @logging
    def get_discrete_selection_column(self, column: Column) -> SettingRecord:
        """
        returns a discrete selection for all the possible parameters in the column that can
        be selected.
        """
        return self._data_getter.get_discrete_selection_column(column)

    @logging
    def get_interval_selection_column(self, column: Column) -> SettingRecord:
        """
        returns an interval selection to select an interval for the corresponding column values.
        """
        return self._data_getter.get_interval_selection_column(column)

from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import List
from typing import Optional
from typing import Type
from typing import Union
from uuid import UUID

from src.data_transfer.content.filter_type import FilterType
from src.data_transfer.record.analysis_data_record import AnalysisDataRecord
from src.data_transfer.record.analysis_record import AnalysisRecord
from src.data_transfer.record.analysis_type_record import AnalysisTypeRecord
from src.data_transfer.record.filter_group_record import FilterGroupRecord
from src.data_transfer.record.filter_record import FilterRecord
from src.data_transfer.record.polygon_record import PolygonRecord
from src.data_transfer.record.settings_record import SettingsRecord
from src.model.analysis_structure.Analysis import Analysis
from src.model.analysis_structure.analysis_structure import AnalysisStructure
from src.model.error_handler import ErrorHandler
from src.model.filter_structure.filter_structure import FilterStructure
from src.model.i_error_handler import IErrorHandler
from src.model.polygon_structure.polygon_structure import PolygonStructure
from src.model.setting_structure.setting_structure import SettingStructure

FACADE_NOT_SET_ERROR: str = "The analysis structure of the ModelFacade has not been set yet. The setter method " \
                            "needs to be called before the AnalysisStructure can be used."


class FilterFacade(IErrorHandler, ABC):
    """
    Abstract class for a filter facade. Defines the methods to manipulate
    filters and filter groups, as well as generate SQL requests.
    """

    @abstractmethod
    def add_filter(self, parent_id: UUID, parameters: FilterRecord) -> UUID:
        """
        Abstract method to add a new filter.

        :param parent_id: The UUID of the parent filter group.
        :type parent_id: UUID
        :param parameters: The parameters for the new filter.
        :type parameters: FilterRecord
        :return: The UUID of the newly created filter.
        :rtype: UUID
        """
        pass

    @abstractmethod
    def add_filter_group(self, parent_id: UUID, parameters: FilterGroupRecord) -> UUID:
        """
        Abstract method to add a new filter group.

        :param parent_id: The UUID of the parent filter group.
        :type parent_id: UUID
        :param parameters: The parameters for the new filter group.
        :type parameters: FilterGroupRecord
        :return: The UUID of the newly created filter group.
        :rtype: UUID
        """
        pass

    @abstractmethod
    def delete(self, component_id: UUID) -> Optional[UUID]:
        """
        Abstract method to delete a filter or filter group.

        :param component_id: The UUID of the filter or filter group to delete.
        :type component_id: UUID
        :return: The UUID of the deleted component, or None if the component was not found.
        :rtype: Optional[UUID]
        """
        pass

    @abstractmethod
    def move_filter_to_group(self, filter_id: UUID, group_id: UUID):
        """
        Abstract method to move a filter to a different group.

        :param filter_id: The UUID of the filter to move.
        :type filter_id: UUID
        :param group_id: The UUID of the group to move the filter to.
        :type group_id: UUID
        """
        pass

    @abstractmethod
    def get_filter(self, filter_id: UUID) -> FilterRecord:
        """
        Abstract method to retrieve the parameters of a filter.

        :param filter_id: The UUID of the filter to retrieve parameters for.
        :type filter_id: UUID
        :return: The parameters of the specified filter.
        :rtype: FilterRecord
        """
        pass

    @abstractmethod
    def get_filter_group(self, filter_group_id: UUID) -> FilterGroupRecord:
        """
        Abstract method to retrieve the parameters of a filter group.

        :param filter_group_id: The UUID of the filter group to retrieve parameters for.
        :type filter_group_id: UUID
        :return: The parameters of the specified filter group.
        :rtype: FilterGroupRecord
        """
        pass

    @abstractmethod
    def get_point_sql_request(self) -> str:
        """
        Abstract method to generate SQL request to filter point data.

        :return: SQL request to filter point data.
        :rtype: str
        """
        pass

    @abstractmethod
    def get_trajectory_sql_request(self) -> str:
        """
        Abstract method to generate SQL request to filter trajectory data.

        :return: SQL request to filter trajectory data.
        :rtype: str
        """
        pass

    @abstractmethod
    def get_filter_types(self) -> List[str]:
        """
        Abstract method to get a list of available filter types.

        :return: A list of available filter types.
        :rtype: List[str]
        """
        pass

    @abstractmethod
    def get_standard_filter(self, filter_type: str) -> FilterRecord:
        """
        Abstract method to get the standard filter parameters for a given filter type.

        :param filter_type: The type of the filter to get the standard parameters for.
        :type filter_type: str
        :return: The standard parameters for the specified filter type.
        :rtype: FilterRecord
        """
        pass

    @abstractmethod
    def get_standard_group(self) -> FilterGroupRecord:
        """
        Abstract method to get the standard parameters for a filter group.

        :return: The standard parameters for a filter group.
        :rtype: FilterGroupRecord
        """
        pass

    @abstractmethod
    def is_polygon_in_use(self, polygon_id: UUID) -> bool:
        """
        checks whether the polygon with the given id is used in one of the filter
        :param polygon_id:  the id of the polygon
        :return:    whether the polygon is used
        """
        pass

    @abstractmethod
    def change_filter(self, uuid: UUID, parameters) -> None:
        """
        Abstract method to change the parameters of a filter.

        :param uuid: The UUID of the filter to change.
        :type uuid: UUID
        :param parameters: The new parameters for the filter.
        :return: None
        """
        pass

    @abstractmethod
    def change_filter_group(self, filter_id: UUID, parameters: FilterGroupRecord, filters: List[UUID]
                            , groups: List[UUID]):
        """
        Abstract method to change the parameters of a filter group.

        :param uuid: The UUID of the filter group to change.
        :param parameters: The new parameters for the filter group.
        """
        pass

    @abstractmethod
    def undo_add(self) -> Optional[UUID]:
        """
        undoes the last addition of a filter component and deletes this filter component without saving it
        :return: the uuid of the deleted component
        """
        pass

    @abstractmethod
    def reconstruct(self) -> Optional[UUID]:
        """
        reconstructs the last deleted filter component
        :return: the uuid
        """
        pass

    @abstractmethod
    def get_point_filters_root(self) -> UUID:
        """
        gets the uuid of the root group of the point filters
        :return: the uuid of the root group of the point filters
        """
        pass

    @abstractmethod
    def get_trajectory_filters_root(self) -> UUID:
        """
        gets th uuid of the root group of the trajectory filters
        :return: the root group of the trajectory filters
        """
        pass


class PolygonFacade(IErrorHandler, ABC):
    """
    This interface is the facade for the polygon structure. It allows manipulating the included polygons.
    """

    @abstractmethod
    def add_polygon(self, polygon: PolygonRecord) -> UUID:
        """
        This method adds a polygon to the polygon structure based on a polygon record

        :param polygon: The polygon to add

        :return: The resulting UUID and a potential error as an IDRecord.
        """

        raise NotImplementedError

    @abstractmethod
    def delete_polygon(self, uuid: UUID) -> bool:
        """
        This method deletes a polygon based on the given uuid.

        :param uuid: The uuid from which the polygon should be deleted

        :return: boolean if the deletion was successful
        """

        raise NotImplementedError

    @abstractmethod
    def get_polygon(self, uuid: UUID) -> Optional[PolygonRecord]:
        """
        This method gets a copy of polygon to a given uuid

        :param uuid: The corresponding uuid

        :return: the polygon copy in a PolygonRecord
        """

        raise NotImplementedError

    @abstractmethod
    def get_all_polygon_ids(self) -> List[UUID]:
        """
        This method returns all uuids that are connected to polygon

        :return: The list of all polygon uuids
        """

        raise NotImplementedError

    @abstractmethod
    def get_all_polygons(self) -> List[PolygonRecord]:
        """
        These methods return a list of copies of all polygons

        :return: PolygonRecord list with all polygon copies
        """

        raise NotImplementedError

    @abstractmethod
    def reconstruct_polygon(self) -> Optional[UUID]:
        """
        This method reconstructs the last polygon deleted. If no polygon was deleted it returns false, if the
        reconstruction was successful it returns true

        :return: If the reconstruction was successful, then uuid
        """

        raise NotImplementedError

    @abstractmethod
    def remove_latest_polygon(self) -> Optional[UUID]:
        """
        This method removes the polygon which was added at last. It DOES NOT add the polygon to the removal stack

        :return: if the removal was successful, then uuid
        """

        raise NotImplementedError


class SettingFacade(IErrorHandler, ABC):
    """
    An abstract class that defines the interface for managing settings.
    """

    @abstractmethod
    def update_settings(self, settings_record: SettingsRecord) -> bool:
        """
        Abstract method to update the settings.

        :param settings_record: The new settings.
        :type settings_record: SettingsRecord
        :return: True if the update was successful, False otherwise.
        :rtype: bool
        """
        pass

    @abstractmethod
    def get_settings_record(self) -> SettingsRecord:
        """
        Abstract method to get the current settings.

        :return: The current settings.
        :rtype: SettingsRecord
        """
        pass

    @abstractmethod
    def get_dictionary(self) -> dict:
        """
        Abstract method to get the current settings as a dictionary.

        :return: The current settings as a dictionary.
        :rtype: dict
        """
        pass

    @abstractmethod
    def load_from_dictionary(self, setting_dictionary: dict) -> bool:
        """
        Abstract method to load settings from a dictionary.

        :param setting_dictionary: The dictionary containing the settings.
        :type setting_dictionary: dict
        :return: True if the load was successful, False otherwise.
        :rtype: bool
        """
        pass


class AnalysisFacade(IErrorHandler, ABC):
    @abstractmethod
    def create_analysis(self, analysis_type: AnalysisTypeRecord) -> Optional[UUID]:
        """
        Create a new analysis.

        :param analysis_type: An object containing the type of analysis to be created.
        :type analysis_type: AnalysisTypeRecord
        :return: UUID of the newly created analysis or None if it could not be created.
        :rtype: Optional[UUID]
        """
        pass

    @abstractmethod
    def get_analysis_parameters(self, analysis_id: UUID) -> AnalysisRecord:
        """
        Retrieve the parameters for a given analysis.

        :param analysis_id: The UUID of the analysis to retrieve the parameters for.
        :type analysis_id: UUID
        :return: An object containing the parameters of the analysis.
        :rtype: AnalysisRecord
        """
        pass

    @abstractmethod
    def edit_analysis(self, analysis_id: UUID, parameters: AnalysisRecord) -> bool:
        """
        Edit the parameters of a given analysis.

        :param analysis_id: The UUID of the analysis to edit.
        :type analysis_id: UUID
        :param parameters: An object containing the new parameters of the analysis.
        :type parameters: AnalysisRecord
        :return: True if the analysis was successfully edited, False otherwise.
        :rtype: bool
        """
        pass

    @abstractmethod
    def get_analyses(self) -> List[AnalysisTypeRecord]:
        """
        Retrieve a list of all available analysis types.

        :return: A list of available analysis types.
        :rtype: List[AnalysisTypeRecord]
        """
        pass

    @abstractmethod
    def delete_analysis(self, analysis_id: UUID) -> bool:
        """
        Delete a given analysis.

        :param analysis_id: The UUID of the analysis to delete.
        :type analysis_id: UUID
        :return: True if the analysis was successfully deleted, False otherwise.
        :rtype: bool
        """
        pass

    @abstractmethod
    def register_analysis_type(self, constructor: Callable[[], object]) -> AnalysisTypeRecord:
        """
        Register a new analysis type.

        :param constructor: A callable object that returns an object representing the new analysis type.
        :type constructor: Callable[[], object]
        :return: An object representing the registered analysis type.
        :rtype: AnalysisTypeRecord
        """
        pass

    @abstractmethod
    def de_register_analysis_type(self, analysis_type: AnalysisTypeRecord) -> bool:
        """
        De-register a given analysis type.

        :param analysis_type: The analysis type to be de-registered.
        :type analysis_type: AnalysisTypeRecord
        :return: True if the analysis type was successfully de-registered, False otherwise.
        :rtype: bool
        """
        pass

    @abstractmethod
    def refresh_analysis(self, analysis_id: UUID) -> bool:
        """
        Refresh the data of a given analysis.

        :param analysis_id: The UUID of the analysis to refresh.
        :type analysis_id: UUID
        :return: True if the analysis was successfully refreshed, False otherwise.
        :rtype: bool
        """
        pass

    @abstractmethod
    def get_analysed_data(self, analysis_id: UUID) -> AnalysisDataRecord:
        """
        Retrieve the analysed data for a given analysis.

        :param analysis_id: The UUID of the analysis to retrieve the analysed data for.
        :type analysis_id: UUID
        :return: An object containing the analysed data.
        :rtype: AnalysisDataRecord
        """
        pass


class ModelFacade(AnalysisFacade, FilterFacade, SettingFacade, PolygonFacade, ErrorHandler):
    """
    A class that acts as a facade to provide a unified interface for interacting with various structures in the system.
    This class extends several other facade classes and
    the ErrorHandler class to manage errors across different structures.
    """

    def get_dictionary(self) -> dict:
        """
        Returns a dictionary representation of the settings structure.
        :return: A dictionary that represents the current settings structure.
        """
        return self._setting_structure.get_dictionary()

    def load_from_dictionary(self, setting_dictionary: dict) -> bool:
        """
        Loads the settings structure from a dictionary.
        :param setting_dictionary: A dictionary that represents the settings structure to be loaded.
        :return: A boolean indicating if the operation was successful.
        """
        return self._setting_structure.load_from_dictionary(setting_dictionary)

    def __init__(self):
        """
        Initializes a new instance of the ModelFacade class and sets its underlying structures to None.
        """
        super().__init__()
        self._analysis_structure: Union[None, AnalysisStructure] = None
        self._filter_structure: Union[None, FilterStructure] = None
        self._setting_structure: Union[None, SettingStructure] = None
        self._polygon_structure: Union[None, PolygonStructure] = None

    def set_analysis_structure(self, analysis_structure: AnalysisStructure):
        """
        Sets the analysis structure used by the facade.
        :param analysis_structure: The AnalysisStructure object to set.
        """
        self._analysis_structure = analysis_structure
        self.add_error_handler(analysis_structure)

    def set_filter_structure(self, filter_structure: FilterStructure):
        """
        Sets the filter structure used by the facade.
        :param filter_structure: The FilterStructure object to set.
        """
        self._filter_structure = filter_structure
        self.add_error_handler(filter_structure)

    def set_setting_structure(self, setting_structure: SettingStructure):
        """
        Sets the setting structure used by the facade.
        :param setting_structure: The SettingStructure object to set.
        """
        self._setting_structure = setting_structure
        self.add_error_handler(setting_structure)

    def set_polygon_structure(self, polygon_structure: PolygonStructure):
        """
        Sets the polygon structure used by the facade.
        :param polygon_structure: The PolygonStructure object to set.
        """
        self._polygon_structure = polygon_structure
        self.add_error_handler(polygon_structure)

    @property
    def __analysis_structure(self) -> AnalysisStructure:
        """
        Gets the analysis structure used by the facade.
        :return: The AnalysisStructure object currently being used by the facade.
        :raises ValueError: If the analysis structure has not been set yet.
        """
        if self._analysis_structure is None:
            raise ValueError(FACADE_NOT_SET_ERROR)
        return self._analysis_structure

    # ------------------------------ #
    # filter:
    # ------------------------------ #
    def add_filter(self, parent_id: UUID, parameters: FilterRecord) -> Optional[UUID]:

        return self._filter_structure.add_filter(parent_id, parameters)

    def add_filter_group(self, parent_id: UUID, parameters: FilterGroupRecord) -> Optional[UUID]:

        return self._filter_structure.add_filter_group(parent_id, parameters)

    def delete(self, component_id: UUID) -> UUID:

        return self._filter_structure.delete_filter_component(component_id)

    def move_filter_to_group(self, filter_id: UUID, group_id: UUID):

        return self._filter_structure.move_filter_to_group(filter_id, group_id)

    def get_filter(self, filter_id: UUID) -> FilterRecord:

        return self._filter_structure.get_filter(filter_id)

    def get_filter_group(self, filter_group_id: UUID) -> FilterGroupRecord:
        return self._filter_structure.get_filter_group(filter_group_id)

    def get_point_sql_request(self) -> Optional[str]:
        filter_str = self._filter_structure.get_point_sql_request()
        if filter_str == "":
            return None
        return filter_str

    def get_trajectory_sql_request(self) -> Optional[str]:
        filter_str = self._filter_structure.get_trajectory_sql_request()
        if filter_str == "":
            return None
        return filter_str

    def get_filter_types(self) -> [FilterType]:

        return self._filter_structure.get_filter_types()

    def get_standard_filter(self, filter_type: str) -> FilterRecord:

        return self._filter_structure.get_standard_filter(filter_type)

    def get_standard_group(self) -> FilterGroupRecord:

        return self._filter_structure.get_standard_group()

    def is_polygon_in_use(self, polygon_id: UUID) -> bool:

        return self._filter_structure.is_polygon_in_use(polygon_id)

    def change_filter(self, polygon_id: UUID, parameters: FilterRecord) -> bool:

        return self._filter_structure.change_filter(polygon_id, parameters)

    def change_filter_group(self, polygon_id: UUID, parameters: FilterGroupRecord, filters: List[UUID]
                            , groups: List[UUID]):

        return self._filter_structure.change_filter_group(polygon_id, parameters, filters, groups)

    def undo_add(self) -> Optional[UUID]:

        return self._filter_structure.undo_add()

    def reconstruct(self) -> Optional[UUID]:

        return self._filter_structure.reconstruct()

    def get_point_filters_root(self) -> UUID:

        return self._filter_structure.get_point_filter_root_id()

    def get_trajectory_filters_root(self) -> UUID:

        return self._filter_structure.get_trajectory_filter_root_id()

    # ------------------------------ #
    # polygon:
    # ------------------------------ #
    def add_polygon(self, polygon_record: PolygonRecord) -> UUID:

        return self._polygon_structure.add_polygon(polygon_record)

    def delete_polygon(self, polygon_id: UUID) -> bool:

        return self._polygon_structure.delete_polygon(polygon_id)

    def get_polygon(self, polygon_id: UUID) -> PolygonRecord:

        return self._polygon_structure.get_polygon(polygon_id)

    def get_all_polygon_ids(self) -> [UUID]:

        return self._polygon_structure.get_all_polygon_ids()

    def remove_latest_polygon(self) -> Optional[UUID]:

        return self._polygon_structure.remove_latest_polygon()

    def get_all_polygons(self) -> List[PolygonRecord]:

        return self._polygon_structure.get_all_polygons()

    def reconstruct_polygon(self) -> Optional[UUID]:

        return self._polygon_structure.reconstruct_polygon()

    # ------------------------------ #
    # setting:
    # ------------------------------ #
    def update_settings(self, settings_record: SettingsRecord) -> bool:

        return self._setting_structure.update_settings(settings_record)

    def get_settings_record(self) -> SettingsRecord:

        return self._setting_structure.get_settings_record()

    # ------------------------------ #
    # analysis:
    # ------------------------------ #
    def create_analysis(self, analysis_type: AnalysisTypeRecord) -> Optional[UUID]:

        return self.__analysis_structure.create_analysis(analysis_type)

    def get_analysis_parameters(self, analysis_id: UUID) -> AnalysisRecord:

        return self.__analysis_structure.get_analysis_parameters(analysis_id)

    def edit_analysis(self, analysis_id: UUID, parameters: AnalysisRecord) -> bool:

        return self.__analysis_structure.edit_analysis(analysis_id, parameters)

    def get_analyses(self) -> [AnalysisTypeRecord]:

        return self.__analysis_structure.get_analysis_types()

    def delete_analysis(self, analysis_id: UUID) -> bool:

        return self.__analysis_structure.delete_analysis(analysis_id)

    def register_analysis_type(self, constructor: Type[Analysis]) -> AnalysisTypeRecord:

        return self.__analysis_structure.register_analysis_type(constructor)

    def de_register_analysis_type(self, analysis_type: AnalysisTypeRecord) -> bool:

        return self.__analysis_structure.de_register_analysis_type(analysis_type)

    def refresh_analysis(self, analysis_id: UUID) -> AnalysisDataRecord:

        return self.__analysis_structure.refresh(analysis_id)

    def get_analysed_data(self, analysis_id: UUID) -> AnalysisDataRecord:

        return self.__analysis_structure.get_analysed_data(analysis_id)

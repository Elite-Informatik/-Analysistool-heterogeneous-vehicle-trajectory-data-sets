from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from uuid import UUID
from uuid import uuid4

from src.data_transfer.content import Column
from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.exception import ExecutionFlowError
from src.data_transfer.exception import InvalidUUID
from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import AnalysisTypeRecord
from src.model.analysis_structure.Analysis import Analysis
from src.model.analysis_structure.analysis_factory import AnalysisFactory
from src.model.analysis_structure.ianalysis_structure import IAnalysisStructure
from src.model.analysis_structure.spatial_analysis.path_daytime_analysis import PathDaytimeAnalysis
from src.model.analysis_structure.spatial_analysis.path_time_analysis import PathTimeAnalysis
from src.model.analysis_structure.spatial_analysis.polygon_consumer_analysis import PolygonFacadeConsumer
from src.model.analysis_structure.spatial_analysis.source_destination_analysis import SourceDestinationAnalysis
from src.model.error_handler import ErrorHandler
from src.model.facade_consumer.data_request_consumer import DataRequestConsumer
from src.model.polygon_structure.ipolygon_structure import IPolygonStructure


class AnalysisStructure(ErrorHandler, DataRequestConsumer, IAnalysisStructure):
    """
    Class representing the structure of an analysis.
    It contains a map of all the analyses that have been created,
    a list of all the analysis types that have been registered,
    as well as a factory for creating new analyses and the current analysis type being created.
    """

    def __init__(self):
        """
        Initializes the analysis structure with an empty map of analyses, an empty list of analysis types, an instance
        of the AnalysisFactory and None as the current analysis type.
        """
        super(AnalysisStructure, self).__init__()
        self._analysis_map: Dict[UUID, Analysis] = {}
        self._analysis_type_list: [AnalysisTypeRecord] = []
        self._factory: AnalysisFactory = AnalysisFactory()
        self.__polygon_structure: Optional[IPolygonStructure] = None
        self.register_analysis_type(constructor=PathTimeAnalysis)
        self.register_analysis_type(constructor=SourceDestinationAnalysis)
        self.register_analysis_type(constructor=PathDaytimeAnalysis)

    def set_polygon_structure(self, polygon_structure: IPolygonStructure) -> None:
        """
        Sets the polygon structure, so it can be used by the analyses that require knowledge of the polygons.
        :param polygon_structure: The polygon structure
        :return: None
        """
        self.__polygon_structure = polygon_structure

    @property
    def _polygon_structure(self) -> IPolygonStructure:
        """
        A guard property to ensure that the polygon structure can only be accessed if set previously.
        :returns the polygon structure if set.
        :raises an ExecutionFlowError if the polygon structure is attempted to be accessed before set.
        """
        if self.__polygon_structure is None:
            raise ExecutionFlowError("Polygon-structure should be set before using it.")
        return self.__polygon_structure

    def edit_analysis(self, analysis_id: UUID, parameters: AnalysisRecord) -> bool:
        """
        Resets the analysis parameters acting as an edit option to change the analysis after creation.
        Necessary as an analysis is always created as default and has to be set afterwards.
        :param analysis_id: The uuid of the analysis to be edited.
        :param parameters: The new parameters of the analysis.
        :returns a bool signifying if the process was a success or not.
        """
        if analysis_id not in self._analysis_map:
            raise InvalidUUID("The analysis id ist not valid.")

        return self._analysis_map[analysis_id].set_analysis_parameters(parameters)

    def get_analysis_parameters(self, analysis_id: UUID) -> AnalysisRecord:
        """
        Gets the parameters of
        :param analysis_id:
        :return:
        """
        if analysis_id not in self._analysis_map:
            raise InvalidUUID("The analysis id ist not valid.")

        return self._analysis_map[analysis_id].get_required_analysis_parameter()

    def delete_analysis(self, analysis_id: UUID) -> bool:
        """
        Deletes the analysis with the specified id from the map of analyses.
        :param analysis_id: The id of the analysis to delete.
        :return: True if the analysis was deleted successfully, False otherwise.
        :raise ValueError: If the analysis_id is invalid.
        """
        if analysis_id not in self._analysis_map:
            raise InvalidUUID("Invalid analysis_id")
        del self._analysis_map[analysis_id]
        return True

    def register_analysis_type(self, constructor: Type[Analysis]) -> AnalysisTypeRecord:
        """
        Registers a new analysis type using the provided constructor.
        :param constructor: The constructor for the analysis type to be registered.
        :return: The AnalysisTypeRecord of the newly registered analysis type.
        """
        analysis_type_id = self._factory.register_analysis(constructor)
        name = constructor().get_name()
        record = AnalysisTypeRecord(name, analysis_type_id)
        self._analysis_type_list.append(record)
        return record

    def de_register_analysis_type(self, analysis_type: AnalysisTypeRecord) -> bool:
        """
        Removes an analysis type from the AnalysisStructure.
        :param analysis_type: The AnalysisTypeRecord of the analysis type to be removed
        :return: True if the analysis type was deleted successfully, False otherwise.
        """
        if analysis_type not in self._analysis_type_list:
            return False
        removed = self._factory.de_register_analysis(analysis_type.uuid)
        if removed:
            self._analysis_type_list.remove(analysis_type)
        return removed

    def create_analysis(self, analysis_type: AnalysisTypeRecord) -> Optional[UUID]:
        """
        Creates an analysis and if necessary supplies the analysis with the consumer dependent classes.
        :param analysis_type:
        :return:
        """

        analysis_id = uuid4()
        analysis = self._factory.create_analysis(analysis_type.uuid)
        self._analysis_map[analysis_id] = analysis
        # The reason isistance is used here is that the class itself should not be able to decide what it gets.
        # This is for security as the scripts are imported and should not be able to access things such as the polygons.
        # Since internal analyses are treated the same as external ones they need to be checked in a way as below.
        if isinstance(analysis, PolygonFacadeConsumer):
            if len(self._polygon_structure.get_all_polygons()) == 0:
                self.throw_error(ErrorMessage.NOT_ENOUGH_POLYGONS)
                return None
            analysis.set_polygon_structure(self._polygon_structure)
        return analysis_id

    def get_analysis_types(self) -> List[AnalysisTypeRecord]:
        """
        A getter for all the analysis types that can be created.
        :return: An arraylist of AnalysisTypeRecords describing all analysis types.
        """
        return self._analysis_type_list.copy()

    def get_analysed_data(self, analysis_id: UUID) -> AnalysisDataRecord:
        """
        Runs the by the id specified analysis.
        :param analysis_id: The id of the to be run analysis
        :return: An AnalysisDataRecord containing all the analysed data prepared for the also specified view
        type to be displayed as.
        """
        analysis = self._analysis_map.get(analysis_id)
        if analysis is None:
            raise InvalidUUID("Invalid analysis_id")
        return analysis.analyse(self.data_request.get_rawdata([Column.get_column_from_str(col_str)
                                                               for col_str in analysis.get_required_columns()]).data)

    def refresh(self, analysis_id: UUID) -> AnalysisDataRecord:
        """
        Refreshes an analysis and returns the newly analysed data.
        :param analysis_id: The id of the analysis to be refreshed.
        :return: An AnalysisDataRecord containing all the analysed data prepared for the also specified view
        type to be displayed as.
        """
        return self.get_analysed_data(analysis_id)

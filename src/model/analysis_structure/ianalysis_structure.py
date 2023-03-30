from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional
from typing import Type
from uuid import UUID

from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import AnalysisTypeRecord
from src.model.analysis_structure.Analysis import Analysis


class IAnalysisStructure(ABC):
    """
    Class representing the structure of an analysis.
    It contains a map of all the analyses that have been created,
    a list of all the analysis types that have been registered,
    as well as a factory for creating new analyses and the current analysis type being created.
    """

    @abstractmethod
    def edit_analysis(self, analysis_id: UUID, parameters: AnalysisRecord) -> bool:
        """
        Resets the analysis parameters acting as an edit option to change the analysis after creation.
        Necessary as an analysis is always created as default and has to be set afterwards.
        :param analysis_id: The uuid of the analysis to be edited.
        :param parameters: The new parameters of the analysis.
        :returns a bool signifying if the process was a success or not.
        """
        pass

    @abstractmethod
    def get_analysis_parameters(self, analysis_id: UUID) -> AnalysisRecord:
        """
        Returns the parameters in an AnalysisRecord that can be changed in an Analysis.
        :param analysis_id: The id of the analysis as an UUID
        :returns: The AnalysisRecord containing the selections that can be made for the given analysis.
        """
        pass

    @abstractmethod
    def delete_analysis(self, analysis_id: UUID) -> bool:
        """
        Deletes the analysis with the specified id from the map of analyses.
        :param analysis_id: The id of the analysis to delete.
        :return: True if the analysis was deleted successfully, False otherwise.
        :raise ValueError: If the analysis_id is invalid.
        """
        pass

    @abstractmethod
    def register_analysis_type(self, constructor: Type[Analysis]) -> AnalysisTypeRecord:
        """
        Registers a new analysis type using the provided constructor.
        :param constructor: The constructor for the analysis type to be registered.
        :return: The AnalysisTypeRecord of the newly registered analysis type.
        """
        pass

    @abstractmethod
    def de_register_analysis_type(self, analysis_type: AnalysisTypeRecord) -> bool:
        """
        Removes an analysis type from the AnalysisStructure.
        :param analysis_type: The AnalysisTypeRecord of the analysis type to be removed
        :return: True if the analysis type was deleted successfully, False otherwise.
        """
        pass

    @abstractmethod
    def create_analysis(self, analysis_type: AnalysisTypeRecord) -> Optional[UUID]:  # AnalysisRecord:
        """
        creates a new analysis of the given type
        :param analysis_type:   the analysis type
        :return:                the generated uuid of the new analysis
        """
        pass

    @abstractmethod
    def get_analysis_types(self) -> List[AnalysisTypeRecord]:
        """
        gets all available analysis types
        :return:    all available analysis types
        """
        pass

    @abstractmethod
    def get_analysed_data(self, analysis_id: UUID) -> AnalysisDataRecord:
        """
        Runs the by the id specified analysis.
        :param analysis_id: The id of the to be run analysis
        :return: An AnalysisDataRecord containing all the analysed data prepared for the also specified view
        type to be displayed as.
        """
        pass

    @abstractmethod
    def refresh(self, analysis_id: UUID) -> AnalysisDataRecord:
        """
        Refreshes an analysis and returns the newly analysed data.
        :param analysis_id: The id of the analysis to be refreshed.
        :return: An AnalysisDataRecord containing all the analysed data prepared for the also specified view
        type to be displayed as.
        """
        pass

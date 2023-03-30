from typing import Dict
from typing import Type
from uuid import UUID
from uuid import uuid4

from src.data_transfer.exception.custom_exception import IllegalAnalysisError
from src.model.analysis_structure.Analysis import Analysis


class AnalysisFactory:
    """
    The analysis factory is responsible for creating analyses.
    It allows dynamic addition and deletion of analysis types.
    """

    def __init__(self):
        """
        The constructor of the AnalysisFactory initializing the analysis_map.
        """
        self._analysis_map: Dict[UUID, Type[Analysis]] = {}

    def create_analysis(self, analysis_type_id: UUID) -> Analysis:
        """
        Creates an instance of the specified analysis using the provided parameters.
        :param analysis_type_id: The unique identifier of the analysis type to create.
        :return: An instance of the specified analysis.
        :raise ValueError: If the analysisTypeId is not registered or the parameters are invalid.
        """
        if analysis_type_id not in self._analysis_map:
            raise ValueError("Invalid analysis_type_id")
        return self._analysis_map[analysis_type_id]()

    def register_analysis(self, constructor: Type[Analysis]) -> UUID:
        """
        Registers a new analysis type with the factory.
        :param constructor: A supplier function that returns an instance of the analysis type.
        :return: A unique identifier for the analysis type.
        :raise ValueError: If the constructor is not valid.
        """
        try:
            analysis = constructor()
        except Exception:
            raise IllegalAnalysisError("The imported analysis cannot be instantiated.")
        else:
            if not isinstance(analysis, Analysis):
                raise IllegalAnalysisError("The imported analysis is not of type Analysis.")

        uuid = uuid4()
        self._analysis_map[uuid] = constructor
        return uuid

    def de_register_analysis(self, uuid: UUID) -> bool:
        """
        Removes a specific analysis type from the factory by its unique ID.

        :param uuid: The unique ID of the analysis type to remove
        :return: True if the operation was successful, False otherwise
        """
        if uuid in self._analysis_map:
            self._analysis_map.pop(uuid)
            return True
        return False

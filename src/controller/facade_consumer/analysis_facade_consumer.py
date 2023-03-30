from abc import ABC
from typing import Optional

from src.model.model_facade import AnalysisFacade


class AnalysisFacadeConsumer(ABC):
    """
    This abstract class defines the basic functionality for all classes that need to use the AnalysisFacade.
    """

    def __init__(self):
        self._analysis_facade: Optional[AnalysisFacade] = None

    @property
    def analysis_facade(self) -> AnalysisFacade:
        """
        A property that returns the AnalysisFacade instance.

        :raises: ValueError if the AnalysisFacade has not been set yet.
        :return: an instance of the AnalysisFacade class
        """
        if self._analysis_facade is None:
            raise ValueError("The analysis facade needs to be set before using {name}.".format(name=self.__str__()))
        return self._analysis_facade

    def set_analysis_facade(self, analysis_facade: AnalysisFacade):
        """
        This method is used to set the AnalysisFacade for the class.

        :param analysis_facade: an instance of the AnalysisFacade class
        """
        self._analysis_facade = analysis_facade

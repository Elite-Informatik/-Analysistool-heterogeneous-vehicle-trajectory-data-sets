from abc import ABC
from typing import Optional

from src.executable_component import ExecutableComponent


class ExecutionComponentConsumer(ABC):
    """
    This abstract class defines the basic functionality for all classes that need to use the AnalysisFacade.
    """

    def __init__(self):
        self._execution_component: Optional[ExecutableComponent] = None

    @property
    def application_execution_facade(self) -> ExecutableComponent:
        """
        A property that returns the AnalysisFacade instance.

        :raises: ValueError if the AnalysisFacade has not been set yet.
        :return: an instance of the AnalysisFacade class
        """
        if self._execution_component is None:
            raise ValueError("The analysis facade needs to be set before using {name}.".format(name=self.__str__()))
        return self._execution_component

    def add_execution_components(self, execution_component: ExecutableComponent):
        """
        This method is used to set the AnalysisFacade for the class.

        :param execution_component: an instance of the AnalysisFacade class
        """
        self._execution_component = execution_component

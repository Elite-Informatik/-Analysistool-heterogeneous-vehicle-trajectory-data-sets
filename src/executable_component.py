from abc import ABC
from abc import abstractmethod


class ExecutableComponent(ABC):
    """
    The Executable Component class describes all big components in the program that need to be started or stopped.
    """

    @abstractmethod
    def start(self):
        """
        Starts the component.
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Stops the component.
        """
        pass

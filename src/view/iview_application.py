from abc import ABC

from src.controller.controller import IController


class IViewApplication(ABC):
    """
    This Interface defines all Methods that are required to be able to integrate the View in the application.
    """

    def set_controller(self, controller: IController):
        """
        Sets the controller with which the View communicates
        """
        pass

    def start(self):
        """
        Starts the View
        """
        pass

    def stop(self):
        """
        Stops the View
        """
        pass

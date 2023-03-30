from abc import ABC

from src.data_transfer.content.logger import logging


class ApplicationFacade(ABC):
    """
    represents an interface for an application
    """

    @logging
    def start(self):
        """
        starts the application
        """
        pass

    @logging
    def stop(self):
        """
        stops the application
        """
        pass

from abc import ABC

from src.controller.idata_request_facade import IDataRequestFacade


class DataRequestConsumer(ABC):
    """
    This consumer represents classed that need information about the database.
    """

    def __init__(self):
        """
        Constructor for a new Consumer
        """
        self.data_request: IDataRequestFacade = None

    def set_data_request(self, data_request: IDataRequestFacade):
        """
        Sets the information data facade

        :param data_request: the facade to set
        """
        self.data_request: IDataRequestFacade = data_request

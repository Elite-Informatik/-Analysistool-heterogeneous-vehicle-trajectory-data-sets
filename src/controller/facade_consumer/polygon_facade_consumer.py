from abc import ABC
from typing import Optional

from src.model.model_facade import PolygonFacade


class PolygonFacadeConsumer(ABC):
    """
    This abstract class defines the basic functionality for all classes that need to use the PolygonFacade.
    """

    def __init__(self):
        self._polygon_facade: Optional[PolygonFacade] = None

    @property
    def polygon_facade(self) -> PolygonFacade:
        """
        Property getter for the PolygonFacade. Raises a ValueError if the facade has not been set.

        :return: the PolygonFacade instance
        :raises: ValueError if the facade has not been set
        """
        if self._polygon_facade is None:
            raise ValueError("The PolygonFacade needs to be set before using {name}.".format(name=self.__str__()))
        return self._polygon_facade

    def set_polygon_facade(self, polygon_facade: PolygonFacade):
        """
        This method is used to set the PolygonFacade for the class.

        :param polygon_facade: an instance of the PolygonFacade class
        """
        self._polygon_facade = polygon_facade

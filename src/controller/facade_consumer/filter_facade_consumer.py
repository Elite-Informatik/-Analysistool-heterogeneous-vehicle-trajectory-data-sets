from abc import ABC
from typing import Optional

from src.model.model_facade import FilterFacade


class FilterFacadeConsumer(ABC):
    """
    This abstract class defines the basic functionality for all classes that need to use the IFilterFacade.
    """

    def __init__(self):
        self._filter_facade: Optional[FilterFacade] = None

    @property
    def filter_facade(self) -> FilterFacade:
        """
        Property getter for the IFilterFacade. Raises a ValueError if the facade has not been set.

        :return: the IFilterFacade instance
        :raises: ValueError if the facade has not been set
        """
        if self._filter_facade is None:
            raise ValueError("The IFilterFacade needs to be set before using {name}.".format(name=self.__str__()))
        return self._filter_facade

    def set_filter_facade(self, filter_facade: FilterFacade):
        """
        This method is used to set the IFilterFacade for the class.

        :param filter_facade: an instance of the IFilterFacade class
        """
        self._filter_facade = filter_facade

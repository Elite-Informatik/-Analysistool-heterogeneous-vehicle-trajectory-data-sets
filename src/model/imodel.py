from abc import ABC
from typing import Union

from src.model.model_facade import ModelFacade


class IModel(ABC):
    """
    An abstract base class that defines the interface for a model in the system.
    """

    @property
    def model_facade(self) -> Union[ModelFacade, None]:
        """
        Gets the ModelFacade object used by the model.
        :return: The ModelFacade object used by the model.
        """
        return None

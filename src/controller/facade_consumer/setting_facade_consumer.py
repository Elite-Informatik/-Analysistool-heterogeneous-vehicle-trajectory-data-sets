from abc import ABC
from typing import Optional

from src.model.model_facade import SettingFacade


class SettingFacadeConsumer(ABC):
    """
    This abstract class defines the basic functionality for all classes that need to use the SettingFacade.
    """

    def __init__(self):
        self._setting_facade: Optional[SettingFacade] = None

    @property
    def setting_facade(self) -> SettingFacade:
        """
        Property getter for the SettingFacade. Raises a ValueError if the facade has not been set.

        :return: the SettingFacade instance
        :raises: ValueError if the facade has not been set
        """
        if self._setting_facade is None:
            raise ValueError("The SettingFacade needs to be set before using {name}.".format(name=self.__str__()))
        return self._setting_facade

    def set_setting_facade(self, setting_facade: SettingFacade):
        """
        This method is used to set the SettingFacade for the class.

        :param setting_facade: an instance of the SettingFacade class
        """
        self._setting_facade = setting_facade

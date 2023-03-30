from abc import ABC
from typing import Optional

from src.view.user_input_request.user_input_request import UserInputRequestFacade


class UserInputRequestFacadeConsumer(ABC):
    """
    This abstract class defines the basic functionality for all classes that need to use the UserInputRequestFacade.
    """
    failure_request: str = "Fail"

    def __init__(self):
        self._user_input_request_facade: Optional[UserInputRequestFacade] = None

    @property
    def user_input_request_facade(self) -> UserInputRequestFacade:
        """
        Property getter for the UserInputRequestFacade. Raises a ValueError if the facade has not been set.

        :return: the UserInputRequestFacade instance
        :raises: ValueError if the facade has not been set
        """
        if self._user_input_request_facade is None:
            raise ValueError("The UserInputRequestFacade needs to be set before using {name}."
                             .format(name=self.__str__()))
        return self._user_input_request_facade

    def set_user_input_request_facade(self, user_input_request_facade: UserInputRequestFacade):
        """
        This method is used to set the UserInputRequestFacade for the class.

        :param user_input_request_facade: an instance of the UserInputRequestFacade class
        """
        self._user_input_request_facade = user_input_request_facade

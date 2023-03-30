from abc import ABC

from src.executable_component import ExecutableComponent
from src.view.event_handler.event_handler import IEventHandlerNotify
from src.view.user_input_request.user_input_request import UserInputRequestFacade


class IView(ExecutableComponent, ABC):
    """
    Interface that defines methods which return the provided interface of the view.
    The methods can be used by other components to gain access to the provided interface of the view.
    """

    def event_handler(self) -> IEventHandlerNotify:
        """
        Returns the Notify interface of the eventhandler. Events can be notified to the
        view via this interface.
        """
        pass

    def user_input_request(self) -> UserInputRequestFacade:
        """
        Returns the UserInputRequest component. The component can be used by other components to get
        input from the user or to send messages, warnings and errors to the user.
        """
        pass

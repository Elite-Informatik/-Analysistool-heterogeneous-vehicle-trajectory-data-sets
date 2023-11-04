"""
Errorhandler Modul contains abstract errorhandler class.
"""
from abc import ABC
from typing import List

from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.record import ErrorRecord
from src.model.i_error_handler import IErrorHandler

DEF_MSG: str = ""


class ErrorHandler(IErrorHandler, ABC):
    """
    ErrorHandler Class is a Composite for handling Model errors. Errors can be set and accessed.
    """

    def __init__(self):
        IErrorHandler.__init__(self)
        self._error_handlers = list()
        self._errors = list()

    def add_error_handler(self, handler: 'ErrorHandler') -> None:
        """
        Adds error handler to the composite.
        :param handler: the handler to be added.
        """
        assert issubclass(handler.__class__, ErrorHandler)
        self._error_handlers.append(handler)

    def remove_error_handler(self, handler: 'ErrorHandler') -> None:
        """
        Removes error handler from the composite.
        :param handler: the handler to be removed.
        """
        assert issubclass(handler.__class__, ErrorHandler)
        self._error_handlers.remove(handler)

    def get_errors(self, clear: bool = True) -> List[ErrorRecord]:
        """
        Gets all errors from the composite.
        :return: All errors from the object and all underlying objects.
        """
        errors: List[ErrorRecord] = self._errors
        if clear:
            self._errors = list()
        for handler in self._error_handlers:
            errors.extend(handler.get_errors())

        return list(set(errors))

    def error_occurred(self) -> bool:
        """
        Returns whether an error has occurred.
        :return: Whether an error has occurred. True if it has, False otherwise.
        """
        return len(self.get_errors(clear=False)) > 0

    def throw_error(self, error: ErrorMessage, msg: str = DEF_MSG) -> None:
        """
        Intern method for throwing an error.
        :param error: the Error to be thrown.
        :param msg: the message to be thrown.
        """
        assert isinstance(error, ErrorMessage)
        self._errors.append(ErrorRecord(error, msg))

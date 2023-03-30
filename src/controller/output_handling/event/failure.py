from dataclasses import dataclass

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class Failure(Event):
    """
    Event thrown when an error occurred
    """

    _message: str

    @property
    def message(self):
        """
        the error message
        """
        return self._message

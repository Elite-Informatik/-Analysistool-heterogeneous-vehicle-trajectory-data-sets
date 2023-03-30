from dataclasses import dataclass

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class DatasetOpened(Event):
    """
    Event is thrown when a new dataset is opened successfully.
    """
    pass

from dataclasses import dataclass

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class DatasetExported(Event):
    """
    Event is thrown if a new dataset is exported successfully.
    """

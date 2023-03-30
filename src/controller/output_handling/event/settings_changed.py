from dataclasses import dataclass

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class SettingsChanged(Event):
    """
    Event is thrown when the trajectory data needs to be refreshed.
    """
    pass

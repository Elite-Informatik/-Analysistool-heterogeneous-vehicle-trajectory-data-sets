from dataclasses import dataclass

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class RefreshTrajectoryData(Event):
    """
    Event is thrown when the trajectories of the application are refreshed.
    """
    pass

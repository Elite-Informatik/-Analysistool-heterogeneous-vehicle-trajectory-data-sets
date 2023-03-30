from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class Event(ABC):
    """
    Interface representing an events that can be sent from a Command to the EventManager. They only store IDs.
    Each Event is a @dataclass, frozen  and thus immutable. They use @property to access the stored IDs.
    @dataclass: https://docs.python.org/3/library/dataclasses.html?highlight=dataclass#module-dataclasses
    @property: https://docs.python.org/3/library/functions.html#property
    """
    pass

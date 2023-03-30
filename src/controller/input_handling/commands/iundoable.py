from abc import ABC
from abc import abstractmethod


class IUndoable(ABC):
    """
    this interface represents an undoable object
    """

    @abstractmethod
    def undo(self):
        """undoes the command"""
        pass

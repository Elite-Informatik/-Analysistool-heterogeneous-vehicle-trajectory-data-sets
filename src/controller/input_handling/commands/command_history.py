from abc import ABC
from typing import Optional

from src.controller.input_handling.commands.iundoable import IUndoable


class ICommandHistory(ABC):
    """
    This interface represents a command history
    """

    def add_undoable(self, command: IUndoable):
        """adds a new undoable command to the history."""
        pass

    def clear_redoables(self):
        """clears (deletes) all redone command"""
        pass

    def get_redo(self):
        """returns last undone command"""
        pass

    def get_undo(self):
        """returns the last command"""
        pass

    def undo_executed(self):
        """updates command history when a command was undone"""
        pass

    def redo_executed(self):
        """updates command history when a command was redone"""
        pass


class CommandHistory(ICommandHistory):
    """represents a command history that keeps track of all the done, undone and redone command."""

    _history: list
    _pointer: int

    def __init__(self):
        self._history = list()
        self._pointer = -1

    def add_undoable(self, command: IUndoable):

        self._history.append(command)
        self._pointer += 1

    def clear_redoables(self):

        self._history = self._history[0: self._pointer + 1]

    def get_redo(self) -> Optional[IUndoable]:

        if len(self._history) <= self._pointer + 1:
            return None
        else:
            return self._history[self._pointer + 1]

    def get_undo(self) -> Optional[IUndoable]:

        if self._pointer < 0:
            return None
        return self._history[self._pointer]

    def undo_executed(self):

        self._pointer -= 1

    def redo_executed(self):

        self._pointer += 1

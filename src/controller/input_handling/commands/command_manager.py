from abc import ABC
from abc import abstractmethod

from src.controller.input_handling.commands.command import Command
from src.controller.input_handling.commands.command_history import CommandHistory
from src.data_transfer.exception import ExecutionFlowError


class ICommandManager(ABC):
    """represents the ICommandManager: defines an interface for the CommandManager that can be passed to commands."""

    @abstractmethod
    def process_command(self, command: Command):
        """executes the command_structure and updates the command_structure history"""
        pass

    @abstractmethod
    def undo(self) -> bool:
        """undoes the last undoable command_structure
        :return:    True if the command was undone, False otherwise"""
        pass

    @abstractmethod
    def redo(self) -> bool:
        """redoes the last undone command_structure
        :return:    True if the command was redone, False otherwise"""
        pass


class CommandManager(ICommandManager):
    """represents the CommandManager: processes User-Input and executes the commands."""

    def __init__(self):
        self._history = CommandHistory()

    def process_command(self, command: Command):
        """executes the command_structure and updates the command_structure history"""
        command.execute()
        if command.was_successful():
            command.update_command_history(self._history)

    def undo(self):
        """undoes the last undoable command_structure"""
        command = self._history.get_undo()
        if command is not None:
            command.undo()
            return True
        return False

    def redo(self):
        """redoes the last undone command_structure"""
        command = self._history.get_redo()
        if command is not None:
            command.execute()
            return True
        return False

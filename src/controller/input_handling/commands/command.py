from abc import ABC

from src.controller.input_handling.commands.command_history import ICommandHistory


class Command(ABC):
    """abstract command, encapsulates functionality"""

    def __init__(self):
        self._was_successful = True

    def execute(self):
        """executes the command"""
        pass

    def update_command_history(self, history: ICommandHistory):
        """updates the command history after execution (clears the redone command by default)"""
        history.clear_redoables()

    def was_successful(self) -> bool:
        """returns whether the command was successful"""
        return self._was_successful

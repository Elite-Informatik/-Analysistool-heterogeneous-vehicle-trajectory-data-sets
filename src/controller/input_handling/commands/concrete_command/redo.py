from src.controller.input_handling.commands.command import Command
from src.controller.input_handling.commands.command_history import ICommandHistory
from src.controller.input_handling.commands.command_manager import ICommandManager


class RedoCommand(Command):
    """
    represents a command to redo the last undone command
    """

    def __init__(self, command_manager: ICommandManager):
        """
        creates a new RedoCommand
        :param command_manager: the command_manager
        """
        super().__init__()
        self._command_manager = command_manager

    def execute(self):
        """
        redoes the last undone command
        :return:
        """
        self._was_successful = self._command_manager.redo()

    def update_command_history(self, history: ICommandHistory):
        """
        updates the command history
        :param history: the command history
        """
        history.redo_executed()

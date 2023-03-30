from src.controller.input_handling.commands.command import Command
from src.controller.input_handling.commands.command_history import ICommandHistory
from src.controller.input_handling.commands.command_manager import ICommandManager


class UndoCommand(Command):
    """
    represents a command to undo the last executed (undoable) command
    """

    def __init__(self, command_manager: ICommandManager):
        """
        creates a new UndoCommand
        :param command_manager: the command_manager
        """
        super().__init__()
        self._command_manager = command_manager

    def execute(self):
        """
        undoes the last executed (undoable) command
        """
        self._was_successful = self._command_manager.undo()

    def update_command_history(self, history: ICommandHistory):
        """
        updates the command history
        :param history:     the command history
        """
        history.undo_executed()

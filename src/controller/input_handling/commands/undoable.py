from src.controller.input_handling.commands.command import Command
from src.controller.input_handling.commands.command_history import ICommandHistory
from src.controller.input_handling.commands.iundoable import IUndoable


class Undoable(IUndoable, Command):
    """
    represents an undoable command
    """

    def update_command_history(self, history: ICommandHistory):
        """
        updates the command history: clears the redone command and adds itself to the history
        :param history:     the command history
        """
        history.clear_redoables()
        history.add_undoable(self)

    def undo(self):
        """
        undoes the command
        """
        pass

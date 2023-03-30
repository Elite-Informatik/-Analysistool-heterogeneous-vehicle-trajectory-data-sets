from unittest import TestCase

from src.controller.input_handling.commands.command_history import CommandHistory
from src.controller.input_handling.commands.undoable import Undoable


class TestCommand(Undoable):

    def undo(self):
        pass

    def execute(self):
        pass


class CommandHistoryTest(TestCase):
    def test_command_history(self):
        history = CommandHistory()
        command1 = TestCommand()
        command2 = TestCommand()
        command3 = TestCommand()
        history.add_undoable(command1)
        self.assertEqual(history.get_undo(), command1)
        self.assertEqual(history.get_redo(), None)
        history.undo_executed()
        self.assertEqual(history.get_redo(), command1)
        history.clear_redoables()
        self.assertEqual(history.get_redo(), None)
        history.add_undoable(command2)
        history.add_undoable(command3)
        history.undo_executed()
        history.redo_executed()
        self.assertEqual(history.get_redo(), None)

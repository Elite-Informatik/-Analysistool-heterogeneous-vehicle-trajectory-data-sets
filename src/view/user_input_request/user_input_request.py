import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
from tkinter.messagebox import showwarning

from src.data_transfer.record.setting_record import SettingRecord
from src.view.user_interface.selection.selection_dialog import SelectionDialog


class UserInputRequestFacade:
    """
    This class is used by the controller to send messages to the user or to force an input by the user.
    .It uses the dialog factory from the user_interface module to create new dialogs.
    """

    MESSAGE_WINDOW_WIDTH = 200
    MESSAGE_WINDOW_HEIGHT = 400

    def send_warning(self, message: str):
        """
        Sends a Warning which is displayed to the user. Uses the tkinter build in messagebox function
        :param message: message which is displayed in the warning window
        """
        message = self._cut_message(message)
        showwarning(message=message)

    def send_error(self, message: str):
        """
        Sends an Error which is displayed to the user. Uses the tkinter build in messagebox function
        :param message: message which is displayed in the error window
        """
        message = self._cut_message(message)
        showerror(message=message)

    def send_message(self, message: str):
        """
        Sends a normal message to the user. Uses the tkinter build in messagebox function
        :param message: the message
        """
        message = self._cut_message(message)
        showinfo(message=message)

    def ask_acceptance(self, message: str, accept_message="accept?", title: str = "") -> bool:
        """
        Sends a message to the user and waits for an answer
        :param message: the message
        :param accept_message: the message that is displayed next to the checkbox
        :param title: the title of the window
        :return: True if the user accepted the message, False otherwise
        """
        ask_window = tk.Toplevel()
        ask_window.title(title)
        ask_window.resizable(False, False)
        ask_window.grab_set()
        ask_window.focus_set()

        message = self._cut_message(message)
        message = self.set_line_breaks(message, 120)

        message_label = tk.Label(master=ask_window, text=message)
        message_label.pack()

        bool_var = tk.BooleanVar()
        bool_var.set(False)
        accept_box = tk.Checkbutton(master=ask_window, text=accept_message, variable=bool_var)
        accept_box.pack(side=tk.LEFT)

        ok_button = tk.Button(master=ask_window, text="OK",
                              command=lambda: self._execute_window_destruction(ask_window.quit, ask_window.destroy))
        ok_button.pack(side=tk.LEFT)

        ask_window.mainloop()
        return bool_var.get()

    @staticmethod
    def set_line_breaks(message: str, line_length: int) -> str:
        """
        Sets line breaks in a message
        :param message: the message
        :param line_length: the length of a line
        :return: the message with line breaks
        """
        return "\n".join(message[i:i + line_length] for i in range(0, len(message), line_length))

    def request_user_input(self, selections: SettingRecord) -> SettingRecord:
        """
        Sends a request to the user
        """
        selection_dialog = SelectionDialog([selections])
        if selection_dialog.valid_input:
            return selection_dialog.new_setting_records[0]
        return selections

    @staticmethod
    def _cut_message(message: str) -> str:
        if len(message) >= 1000:
            return message[0:1000] + "..."
        return message

    @staticmethod
    def _execute_window_destruction(quit: callable, destroy: callable):
        quit()
        destroy()

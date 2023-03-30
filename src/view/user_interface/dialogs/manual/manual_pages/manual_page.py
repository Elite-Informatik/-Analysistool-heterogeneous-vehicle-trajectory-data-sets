import tkinter as tk
from abc import ABC
from tkinter import scrolledtext


class ManPage(ABC):
    """
    This interface represents an abstract manual page.
    """

    def __init__(self):
        self._base_frame: tk.Frame = None
        self._text_area: scrolledtext.ScrolledText = None

    def build(self, master) -> tk.Frame:
        """
        builds the man page
        :param master:  the master of the man page
        :return:        the frame that holds the man page
        """
        self._base_frame = tk.Frame(master=master)
        self._text_area = scrolledtext.ScrolledText(master=self._base_frame,
                                                    bg="gray90",
                                                    borderwidth=0,
                                                    wrap=tk.WORD,
                                                    font=("Arial", 14))
        self._text_area.config(spacing1=8)  # Spacing above the first line in a block of text
        self._text_area.config(spacing2=8)  # Spacing between the lines in a block of text
        self._text_area.config(spacing3=8)  # Spacing after the last line in a block of text
        self._text_area.tag_config("heading", font=("Arial", 15, "bold"))

    def get_title(self) -> str:
        """
        gets the title of the man page
        :return the title
        """
        pass

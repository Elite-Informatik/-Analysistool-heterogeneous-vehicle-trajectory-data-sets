from tkinter import DISABLED, END

from src.view.user_interface.dialogs.manual.manual_pages.manual_page import ManPage
import tkinter as tk

from src.view.user_interface.ui_util.texts import EnglishTexts


class MapManual(ManPage):
    """
    This manpage contains the manual for the map
    """

    def build(self, master) -> tk.Frame:
        super().build(master)
        self._text_area.insert(END, introduction)
        self._text_area.insert(END, export_heading, "heading")
        self._text_area.insert(END, export_steps)
        self._text_area.insert(END, rawdata_heading, "heading")
        self._text_area.insert(END, rawdata_steps)
        self._text_area.insert(END, rawtraj_heading, "heading")
        self._text_area.insert(END, rawtraj_steps)

        self._text_area.config(state=DISABLED)
        self._text_area.pack(fill="both", expand=True)
        return self._base_frame

    def get_title(self) -> str:
        return EnglishTexts.MAP_MANUAL_TITLE.value


introduction: str = "In this section you can find a manual for the map.\n\n"
export_heading: str = "How to export the current map area:\n"
export_steps: str = "1. Right click on the map view.\n" \
                    "2. Click 'Export'.\n" \
                    "3. Enter directory and file name and press ok.\n\n"
rawdata_heading: str = "How to display the raw data of a datapoint:\n"
rawdata_steps: str = "1. Left click on a datapoint.\n" \
                    "2. Click 'show datapoint data'.\n"\
                    "3. The raw data of the datapoint should now be displayed in a table.\n\n"
rawtraj_heading: str = "How to display the raw data of a trajectory:\n"
rawtraj_steps: str = "1. Left click on a datapoint or line segment.\n" \
                    "2. Click 'show trajectory data'.\n"\
                    "3. The raw data of the trajectory should now be displayed in a table.\n\n"

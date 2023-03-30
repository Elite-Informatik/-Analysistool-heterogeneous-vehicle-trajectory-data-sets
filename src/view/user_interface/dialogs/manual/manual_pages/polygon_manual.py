import tkinter as tk
from tkinter import END, DISABLED

from src.view.user_interface.dialogs.manual.manual_pages.manual_page import ManPage
from src.view.user_interface.ui_util.texts import EnglishTexts


class PolygonManual(ManPage):
    """
    This manpage contains the manual for polygons.
    """

    def build(self, master) -> tk.Frame:
        super().build(master)
        self._text_area.insert(END, introduction)
        self._text_area.insert(END, create_heading, "heading")
        self._text_area.insert(END, create_steps)
        self._text_area.insert(END, delete_heading, "heading")
        self._text_area.insert(END, delete_steps)
        self._text_area.insert(END, use_heading, "heading")
        self._text_area.insert(END, use_steps)

        self._text_area.config(state=DISABLED)
        self._text_area.pack(fill="both", expand=True)
        return self._base_frame

    def get_title(self) -> str:
        return EnglishTexts.POLYGON_MANUAL_TITLE.value


introduction: str = "In this section you can find a manual for polygons.\n\n"
create_heading: str = "How to create a polygon:\n"
create_steps: str = "1. Click on the '+P' button in the map.\n" \
                    "2. Now you are in the polygon generation mode. Click on the map to set the corners of the new polygon." \
                    "When you are finished, click again on the first corner to connect first and last corner of the polygon.\n" \
                    "3. Now a dialog should open. Enter the name and press ok.\n" \
                    "4. The new polygon should now be displayed in the polygon sidebar.\n\n"

delete_heading: str = "How to delete a polygon:\n"
delete_steps: str = "1. Click on the '-P' button in the map.\n" \
                    "2. Now you are in the polygon deletion mode. Click on a polygon to delete it.\n" \
                    "3. Confirm the deletion.\n\n"

use_heading: str = "How to use a polygon:\n"
use_steps: str = "Polygons can be used in filters and in analyses. When creating a polygon filter (area- or transit-filter) " \
                 "or a spatial analysis (e.g. path time analysis), you can select the polygons in the according creation menu." \
                 "If polygons are not used in filters or analyses, they have no effect.\n"

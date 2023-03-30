import tkinter as tk
from tkinter import END, DISABLED

from src.view.user_interface.dialogs.manual.manual_pages.manual_page import ManPage
from src.view.user_interface.ui_util.texts import EnglishTexts


class DataformatManual(ManPage):
    """
    This manpage contains the manual for the uniform data format.
    """

    def build(self, master) -> tk.Frame:
        super().build(master)
        self._text_area.insert(END, introduction)
        self._text_area.insert(END, units_content)

        self._text_area.config(state=DISABLED)
        self._text_area.pack(fill="both", expand=True)
        return self._base_frame

    def get_title(self) -> str:
        return EnglishTexts.DATAFORMAT_MANUAL_TITLE.value


introduction: str = "In this section you can find a manual for the uniform dataformat.\n\n"

units_content: str = "When importing a dataset, it will be converted into the uniform dataformat. " \
                     "In the following you can find a list of all dataset columns and its units:\n" \
                     "ID: UUID\n" \
                     "TRAJECTORY_ID: UUID\n" \
                     "DATE: DD.MM.YYYY\n" \
                     "TIME: HH:MM:SS\n" \
                     "LATITUDE: Degrees\n" \
                     "LONGITUDE: Degrees\n" \
                     "SPEED: km/h\n" \
                     "SPEED_LIMIT: km/h\n" \
                     "ACCELERATION: m/s^2\n" \
                     "SPEED_DIRECTION: Degrees\n" \
                     "ACCELERATION_DIRECTION: Degrees\n" \
                     "ROAD_TYPE: String\n" \
                     "OSM_ROAD_ID: String\n" \
                     "ONE_WAY_STREET: Boolean\n" \
                     "VEHICLE_TYPE: String\n" \
                     "FILTERED: Boolean\n\n"

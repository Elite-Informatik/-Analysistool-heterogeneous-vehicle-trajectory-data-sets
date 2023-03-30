from tkinter import END, DISABLED

from src.view.user_interface.dialogs.manual.manual_pages.manual_page import ManPage
import tkinter as tk

from src.view.user_interface.ui_util.texts import EnglishTexts


class DatasetManual(ManPage):
    """
    This manpage contains the manual for datasets.
    """

    def build(self, master) -> tk.Frame:
        super().build(master)
        self._text_area.insert(END, introduction)
        self._text_area.insert(END, import_heading, "heading")
        self._text_area.insert(END, import_steps)
        self._text_area.insert(END, export_heading, "heading")
        self._text_area.insert(END, export_steps)
        self._text_area.insert(END, delete_heading, "heading")
        self._text_area.insert(END, delete_steps)

        self._text_area.config(state=DISABLED)
        self._text_area.pack(fill="both", expand=True)
        return self._base_frame

    def get_title(self) -> str:
        return EnglishTexts.DATASET_MANUAL_TITLE.value

introduction: str = "In this section you can find a manual for importing, deleting and working with datasets.\n\n"
import_heading: str = "How to import a new dataset:\n"
import_steps: str = "1. Click on 'File'/ 'Import Dataset' button in the menu bar or on the 'Import Dataset' button in the start window.\n" \
                    "2. Select the dataset format and enter a name for the new dataset.\n" \
                    "3. Depending on the dataset format you have to select one or multiple files you want to import:\n" \
                    "   HighD: Select the track, recording and recording meta file.\n" \
                    "   FCD Ui: Select only one CSV file.\n" \
                    "4. After pressing ok, the dataset will be scanned for corruptions. This can take some time. " \
                    "   If the dataset contains corruptions, you will receive a warning. Accept the curruptions or cancel the import.\n" \
                    "5. If the corruptions were accepted, the dataset will be imported. This will take some time. \n" \
                    "6. Finally, the map view will be opened, displaying the new dataset.\n\n"

export_heading: str = "How to export the currently opened and filtered dataset:\n"
export_steps: str = "1. Click on the 'File'/ 'Export Dataset' button in the menu bar.\n" \
                    "2. Select the path and press ok.\n\n"

delete_heading: str = "How to delete a dataset:\n"
delete_steps: str = "1. Click on the 'Settings'/ 'Datasets' button in the menu bar.\n" \
                    "2. Right click on a dataset and click 'delete'.\n" \
                    "3. Confirm the deletion.\n\n"



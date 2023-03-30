import tkinter as tk
import uuid

from src.data_transfer.record import AnalysisTypeRecord
from src.view.user_interface.dialogs.create_analysis import CreateAnalysisDialog


class CreateAnalysisDialogTest:
    pass


if __name__ == "__main__":
    root = tk.Tk()
    dialog = CreateAnalysisDialog([AnalysisTypeRecord('anlysis1', uuid.uuid1())])
    print(dialog.selected_analysis_type)

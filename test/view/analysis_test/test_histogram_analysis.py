from datetime import datetime
import tkinter as tk

import pandas as pd
from matplotlib import pyplot as plt
from pandas import DataFrame

from src.data_transfer.record import DataRecord
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses.histogram_analysis_view import \
    HistogramAnalysisView


class HistogramAnalysisTest:

    def test_histogram_analysis(self):
        # create root frame
        root = tk.Tk()
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        base_frame = tk.Frame(master=root, height=500, width=500)
        base_frame.columnconfigure(0, weight=1)
        base_frame.rowconfigure(0, weight=1)
        base_frame.grid(row=0, column=0, sticky="nsew")

        data_dict = {'values': ["1", "2", "4", "3", "5", "6", "7"],#, "acht", "neun", "zehn", "elf", "zwölf"],
                     'occurencies': [1,2, 3, 4, 5, 6, 7]} # 8, 9, 10, 11, 12]}
        df = DataFrame(data_dict)

        # draw plot
        histogram_analysis_view = HistogramAnalysisView(DataRecord('data_record', (), df), None)
        histogram_analysis_view.build(master=base_frame).pack(fill="both", expand=True)
        root.mainloop()


if __name__ == "__main__":
    histogram_test = HistogramAnalysisTest()
    histogram_test.test_histogram_analysis()


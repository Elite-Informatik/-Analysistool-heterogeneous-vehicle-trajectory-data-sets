import tkinter as tk

from pandas import DataFrame

from src.data_transfer.record import DataRecord
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses.table_analysis_view import \
    TableAnalysisView


class TableAnalysisTest:

    def test_table_analysis(self):
        # create root frame
        root = tk.Tk()
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        base_frame = tk.Frame(master=root, height=500, width=500)
        base_frame.columnconfigure(0, weight=0)
        base_frame.rowconfigure(0, weight=0)

        base_frame.columnconfigure(1, weight=1)
        base_frame.rowconfigure(1, weight=1)
        base_frame.grid(row=0, column=0, sticky="nsew")

        # create data frame
        data_dict = {'value1': [90, 100, 91, 92, 98, 95],
                     'value2': [93, 89, 99, 92, 94, 92]
                     }
        df = DataFrame(data_dict)

        # draw table
        table_analysis_view = TableAnalysisView(DataRecord('data_record', (), df), None)
        table_analysis_view.build(base_frame).pack()
        root.mainloop()


if __name__ == "__main__":
    table_test = TableAnalysisTest()
    table_test.test_table_analysis()

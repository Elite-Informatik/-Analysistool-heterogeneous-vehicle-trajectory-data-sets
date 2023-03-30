import tkinter as tk

from pandas import DataFrame

from src.data_transfer.content import Column
from src.data_transfer.record import DataRecord
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses.barcode_analysis_view import \
    BarcodeAnalysisView


class BarcodeAnalysisTest:

    def test_plot_analysis(self):
        # create root frame
        root = tk.Tk()
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        base_frame = tk.Frame(master=root, height=500, width=500)
        base_frame.columnconfigure(0, weight=1)
        base_frame.rowconfigure(0, weight=1)
        base_frame.grid(row=0, column=0, sticky="nsew")

        # create data frame
        data_dict = {Column.TRAJECTORY_ID.value: [0, 0, 1, 1, 1, 1],
                     Column.ROAD_TYPE.value: [20, 30, 91, 92, 98, 95],
                     Column.VEHICLE_TYPE.value: [50, 70, 99, 92, 94, 92]
                     }
        df = DataFrame(data_dict)

        # draw plot
        plot_analysis_view = BarcodeAnalysisView(DataRecord('data_record', (), df), None)
        plot_analysis_view.build(base_frame).pack(fill="both", expand=True)
        root.mainloop()


if __name__ == "__main__":
    plot_test = BarcodeAnalysisTest()
    plot_test.test_plot_analysis()

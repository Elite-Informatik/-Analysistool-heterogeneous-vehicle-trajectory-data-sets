import tkinter as tk
from datetime import datetime

from pandas import DataFrame

from src.data_transfer.record import DataRecord
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses.heatmap_analysis_view import \
    HeatmapAnalysisView


class HeatmapAnalysisTest:

    def heatmap_analysis_test(self, df):
        # create root frame
        root = tk.Tk()
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        base_frame = tk.Frame(master=root, height=500, width=500)
        base_frame.columnconfigure(0, weight=1)
        base_frame.rowconfigure(0, weight=1)
        base_frame.grid(row=0, column=0, sticky="nsew")

        # draw plot
        heatmap_analysis_view = HeatmapAnalysisView(DataRecord('data_record', (), df), None)
        heatmap_analysis_view.build(base_frame).pack(fill="both", expand=True)
        root.mainloop()


if __name__ == "__main__":
    # harvest = np.zeros((10, 4000))
    #
    # df = DataFrame(harvest)
    #
    # plot_test = HeatmapAnalysisTest()
    # plot_test.heatmap_analysis_test(df)

    data_dict = {
        "time": [datetime.strptime("00:00:05", '%H:%M:%S').time(), datetime.strptime("00:00:01", '%H:%M:%S').time()],
        "speed": [1, 2]
        }
    df = DataFrame(data_dict)
    print(df["time"].dtype)

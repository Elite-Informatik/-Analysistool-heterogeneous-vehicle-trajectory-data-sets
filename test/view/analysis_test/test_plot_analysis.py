import tkinter as tk
from datetime import date
from datetime import datetime

from pandas import DataFrame

from src.data_transfer.content import Column
from src.data_transfer.record import DataRecord
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses.plot_analysis_view import \
    PlotAnalysisView


class PlotAnalysisTest:

    def test_plot_analysis(self):
        # create root frame
        root = tk.Tk()
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        base_frame = tk.Frame(master=root)
        base_frame.columnconfigure(0, weight=1)
        base_frame.rowconfigure(0, weight=1)
        base_frame.grid(row=0, column=0, sticky="nsew")

        # create data frame
        data_dict = {Column.TIME.value: ["00:00:05", "00:00:01"],
                     Column.VEHICLE_TYPE.value: [1, 2]
                     }
        df = DataFrame(data_dict)

        data_dict = {
            Column.ROAD_TYPE.value: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            Column.VEHICLE_TYPE.value: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        }
        df_numeric = DataFrame(data_dict)

        time_string1 = '00:00:05'
        time_string2 = "00:00:01"
        time_obj1 = datetime.strptime(time_string1, '%H:%M:%S').time()
        time_obj2 = datetime.strptime(time_string2, '%H:%M:%S').time()
        default_date = date(2022, 3, 12)
        datetime_obj1 = datetime.combine(default_date, time_obj1)
        datetime_obj2 = datetime.combine(default_date, time_obj2)
        print(datetime_obj1.__repr__())
        print(datetime_obj1.time())
        data_dict = {Column.TIME.value: [datetime_obj1, datetime_obj2],
                     "speed": [1, 2]
                     }
        df_time = DataFrame(data_dict)

        # draw plot
        plot_analysis_view = PlotAnalysisView(DataRecord('data_record', (), df_time), None)
        plot_view = plot_analysis_view.build(base_frame)
        plot_analysis_view._figure.get_axes()[0].get_xticklabels()[0].set_text("hallo")
        plot_view.pack(fill="both", expand=True)
        root.mainloop()


if __name__ == "__main__":
    plot_test = PlotAnalysisTest()
    plot_test.test_plot_analysis()

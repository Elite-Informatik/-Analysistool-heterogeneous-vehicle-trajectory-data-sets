import tkinter
import tkinter as tk
import uuid

from pandas import DataFrame

from src.data_transfer.content import Column
from src.data_transfer.content.analysis_view import AnalysisViewEnum
from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import AnalysisTypeRecord
from src.data_transfer.record import DataRecord
from src.data_transfer.record import FileRecord
from src.data_transfer.record import SettingRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.selection.string_option import StringOption
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.analysis_area import \
    AnalysisArea

analysis_area: AnalysisArea
root: tkinter.Tk


class EventStub:

    def subscribe_analysis_events(self, subscribor):
        pass


class ControllerStub():

    def set(self, area: AnalysisArea, analysis_id: uuid.UUID):
        self._analysis_area = area
        self._analysis_id = analysis_id

    def add_analysis(self, analysis_type: AnalysisTypeRecord):
        self._analysis_area.add_analysis(self._analysis_id)

    def refresh_analysis(self, id: uuid.UUID):
        self._analysis_area.refresh(id)

    def delete_analysis(self, id: uuid.UUID):
        self._analysis_area.delete_analysis(id)

    def change_analysis(self, id: uuid.UUID, settings: AnalysisRecord):
        print("selected value: ", settings.required_data[0].selection.selected)

    def export_file(self, file: FileRecord, selected_path: str):
        file.save(selected_path)

    def import_analysis_type(self, path: str):
        print(path)


class DataRequestStub:

    def get_analysis_types(self):
        options = [AnalysisTypeRecord('anlysis1', uuid.uuid1()), AnalysisTypeRecord('analysis2', uuid.uuid1()),
                   AnalysisTypeRecord('analysis3', uuid.uuid1())]
        return options

    def get_analysis_data(self, id: uuid.UUID):
        return AnalysisDataRecord(data, AnalysisViewEnum.histogram_view)

    def get_analysis_settings(self, id: uuid.UUID):
        return AnalysisRecord(
            (SettingRecord("the first string context", SelectionRecord(["aaa"], StringOption("a*"), range(0, 4))),))


class AnalysisWindowTest:
    pass


if __name__ == "__main__":
    root = tk.Tk()

    # create data frame
    data_dict = {Column.ROAD_TYPE.name: [90, 100, 91, 92, 98, 95],
                 Column.ACCELERATION.name: [93, 89, 99, 92, 94, 92]
                 }
    df = DataFrame(data_dict)
    data = DataRecord('lol', (), df)

    data_request_stub = DataRequestStub()
    event_stub = EventStub()
    controller_stub = ControllerStub()
    analysis_area = AnalysisArea(controller_stub, data_request_stub, event_stub)
    analysis_area_widget = analysis_area.build(None)
    controller_stub.set(analysis_area, uuid.uuid1())
    analysis_area_widget.grid(sticky="nsew")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()

from src.data_transfer.record import SettingRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.selection.bool_discrete_option import BoolDiscreteOption
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.data_transfer.selection.interval_value_option import IntervalValueOption
from src.data_transfer.selection.string_option import StringOption
from src.view.user_interface.selection.selection_window import SelectionWindow


def on_closing():
    print(selection_dialog.new_setting_records == [
        SettingRecord("the first string context", SelectionRecord(["a"], StringOption("a*"), range(0, 4))),
        SettingRecord("the second interval context", SelectionRecord([1], IntervalValueOption(1, 10), range(0, 4))),
        SettingRecord("the third discrete context",
                      SelectionRecord(["grün", "blau"], DiscreteOption(["grün", "blau", "rot", "gelb"]), range(1, 3))),
        SettingRecord("the forth boolean context", SelectionRecord([False], BoolDiscreteOption(), range(1, 3)))])
    selection_dialog.destroy()


if __name__ == "__main__":
    setting_records = [
        SettingRecord("the first string context", SelectionRecord(["aaa"], StringOption("a*"), range(0, 4))),
        SettingRecord("the second interval context", SelectionRecord([1], IntervalValueOption(1, 10), range(1, 2))),
        SettingRecord("the third discrete context",
                      SelectionRecord(["grün", "rot"], DiscreteOption(["grün", "blau", "rot", "gelb"]), range(1, 3))),
        SettingRecord(
            "the forth boolean context aldrskjgai jjrgiojdfvljasr gfljndsrgfjae irjgajdigsjdf gvujsdflkvja äpdrgvjpaojdr",
            SelectionRecord([True], BoolDiscreteOption(), range(1, 3)))]

    selection_dialog = SelectionWindow(setting_records, on_closing)
    selection_dialog.run()

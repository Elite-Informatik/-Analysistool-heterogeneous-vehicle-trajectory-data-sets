from src.data_transfer.record import DataRecord
from src.file.converter.fcd_ui_converter import FCDUIConverter
from src.file.file_facade_manager import FileFacadeManager


def import_data() -> DataRecord:
    file_facade = FileFacadeManager()
    path1: str = "/Users/alexjenke/Documents/KIT/PSE/Beispieldaten/FCD_A5_UI_Sample" \
                 "/part-00000-0c3c17ab-9bbd-46ef-9569-229f2348dcc7-c000.csv"
    paths = [path1]
    inaccuracies = []
    record = file_facade.import_data_files(paths, FCDUIConverter.NAME, True, inaccuracies)
    assert record is not None
    return record
    # print(inaccuracies)
    # record.data.to_csv("/Users/alexjenke/Documents/KIT/PSE/export/result.csv", index=False, sep=";")

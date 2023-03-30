import zipfile

from src.file.file.unpacker.unpacker import Unpacker


class ZipUnpacker(Unpacker):
    """
    Class representing a ZipUnpacker.
    """

    def fits_file_format(self, name: str) -> bool:
        return name.endswith(".zip")

    def unpack_to_folder(self, path: str, new_folder_path: str) -> None:
        with zipfile.ZipFile(path) as zip_ref:
            zip_ref.extractall(new_folder_path)

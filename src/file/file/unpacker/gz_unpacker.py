import gzip
import os

from src.file.file.unpacker.unpacker import Unpacker


class GZUnpacker(Unpacker):
    """
    Class representing a GZUnpacker.
    """

    def fits_file_format(self, name: str) -> bool:
        return name.endswith(".gz")

    def unpack_to_folder(self, path: str, new_folder_path: str) -> None:
        with gzip.open(path, 'rb') as f_in, \
                open(os.path.join(new_folder_path, os.path.basename(os.path.splitext(path)[0])), 'wb') as f_out:
            f_out.write(f_in.read())

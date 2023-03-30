import os
from abc import ABC
from abc import abstractmethod


class Unpacker(ABC):
    """
    Abstract class representing an Unpacker.
    """

    @abstractmethod
    def fits_file_format(self, name: str) -> bool:
        """
        Returns if a file can be unpacked by the class.

        :return: if the file _name represents a file that can be unpacked by the class.
        """
        pass

    def unpack(self, path: str) -> str:
        """
        Unpacks the archive located at the given path and extract the contents to a new folder.

        :param path: path of the archive to unpack
        :return: path of the folder containing the unpacked contents
        """
        new_folder_path = os.path.splitext(path)[0]
        new_folder_path = os.path.join(os.path.dirname(path), os.path.basename(new_folder_path))
        os.makedirs(new_folder_path)
        self.unpack_to_folder(path, new_folder_path)
        return new_folder_path

    @abstractmethod
    def unpack_to_folder(self, path: str, new_folder_path: str) -> None:
        """
        Unpacks the archive located at the given path and extract the contents to a new folder.

        :param path: path of the archive to unpack
        :param new_folder_path: path of the folder containing the unpacked contents
        """
        pass

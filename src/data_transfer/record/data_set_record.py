from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetRecord:
    """
    record containing the metadata of a dataset
    """

    _name: str
    _size: int

    @property
    def name(self):
        """
        the name of the dataset
        """
        return self._name

    @property
    def size(self):
        """
        the size of the dataset
        """
        return self._size

from dataclasses import dataclass

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class FileExported(Event):
    """
    Event is thrown if data is exported successfully.
    """
    _name: str

    @property
    def name(self) -> str:
        """
        Returns the _name of the exported file

        :return: _name of the file
        """
        return self._name

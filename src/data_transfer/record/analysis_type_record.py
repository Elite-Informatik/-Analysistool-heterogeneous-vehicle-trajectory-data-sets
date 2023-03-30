from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AnalysisTypeRecord:
    """
    records that holds the name and the ID of an analysis type
    """

    _name: str
    _uuid: UUID

    @property
    def name(self):
        """
        the name of the analysis type
        """
        return self._name

    @property
    def uuid(self):
        """
        the ID of the analysis type
        """
        return self._uuid

    def __str__(self):
        return self._name

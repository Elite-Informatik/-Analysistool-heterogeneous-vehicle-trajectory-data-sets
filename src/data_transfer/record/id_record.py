from uuid import UUID


class IDRecord:
    """
    A Record that holds an id and defines a string that should be shown in the
    view as a representation for the id
    """

    def __init__(self, id: UUID, representation: str):
        """
        Creates a new IdRecord instance
        :param id: the id
        :param representation: the representation of the id
        """
        self._id = id
        self._representation = representation

    @property
    def id(self) -> UUID:
        """
        returns the id
        """
        return self._id

    @property
    def name(self) -> str:
        """
        returns the name
        """
        return self._representation

    def __str__(self):
        return self._representation

    def __repr__(self):
        """
        returns the representation of the id
        """
        return self._representation

    def __eq__(self, other):
        if not isinstance(other, IDRecord):
            return False
        if other._id != self._id or other._representation != self._representation:
            return False
        return True

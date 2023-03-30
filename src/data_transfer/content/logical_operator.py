from enum import Enum
from typing import List


class LogicalOperator(Enum):
    """
    represents all possible logical operators used by filters groups
    """

    AND = "and"
    OR = "or"

    def join_requests(self, requests: List[str]) -> str:
        """
        joins a list of requests with the logical operator als separator
        """
        return "(" + (" " + self.value + " ").join(requests) + ")"

    def to_string(self):
        """
        returns an upper case string for each logical operator
        """
        return self.value.upper()


LOGICAL_OPERATORS_STRING = [LogicalOperator.AND.to_string(), LogicalOperator.OR.to_string()]

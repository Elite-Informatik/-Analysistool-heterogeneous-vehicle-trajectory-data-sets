from unittest import TestCase

from src.database.database import Database


class TestDatabase(TestCase):
    def setUp(self) -> None:
        self.database = Database()

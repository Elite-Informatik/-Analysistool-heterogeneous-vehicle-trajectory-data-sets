from unittest import TestCase
from uuid import UUID

from src.data_transfer.content.type_check import type_check
from src.data_transfer.content.type_check import type_check_assert
from src.data_transfer.exception import InvalidInput
from src.data_transfer.exception import InvalidUUID


class TestTypeCheck(TestCase):

    @type_check_assert(str)
    def type_checked_assert_function(self, test: str):
        return test

    @type_check(str)
    def type_checked_function(self, test: str):
        return test

    @type_check(UUID)
    def type_checked_uuid_function(self, test: UUID):
        return test

    def test_type_check_assertion(self):
        self.assertEqual(self.type_checked_assert_function("test"), "test")
        with self.assertRaises(AssertionError):
            self.type_checked_assert_function(1)

    def test_type_check(self):
        self.assertEqual(self.type_checked_function("test"), "test")
        with self.assertRaises(InvalidInput):
            self.type_checked_function(1)
        with self.assertRaises(InvalidInput):
            self.type_checked_function(None)

    def test_type_check_uuid(self):
        id_ = UUID("00000000-0000-0000-0000-000000000000")
        self.assertEqual(id_, id_)
        with self.assertRaises(InvalidUUID):
            self.type_checked_uuid_function(None)
        with self.assertRaises(InvalidUUID):
            self.type_checked_uuid_function("test")

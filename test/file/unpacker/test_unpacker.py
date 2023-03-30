from unittest import TestCase

from src.file.file.unpacker.unpacker import Unpacker


class TestUnpacker(TestCase):
    def test_unpack_abstract_class(self):
        with self.assertRaises(TypeError):
            unpacker = Unpacker()

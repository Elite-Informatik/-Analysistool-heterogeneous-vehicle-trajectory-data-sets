import os
from unittest import TestCase

from src.application import Application


class TestApplication(TestCase):
    def test_initialize(self):
        try:
            os.chdir(os.path.join(os.path.dirname(os.getcwd()), 'src'))
            a = Application()
        except Exception as e:
            self.fail(e.args)

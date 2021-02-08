import unittest
from src.CI import app


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_index(self):
        self.assertEqual("Hello :)", app.index())

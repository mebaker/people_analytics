from unittest import TestCase
from people_analytics.__main__ import main


class TestMain(TestCase):
    def test_main(self):
        main()
        self.assertTrue(True)

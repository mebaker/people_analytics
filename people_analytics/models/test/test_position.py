from unittest import TestCase
import pandas as pd
from ..position import Position


class PositionTest(TestCase):
    def test_init(self):
        data = pd.read_csv("./test/data/input/position.csv", na_filter=False).to_dict(
            "records"
        )
        data = list(map(lambda x: Position(x), data))
        self.assertTrue(isinstance(data[0], Position))

    def test_failed_init(self):
        self.assertRaises(Exception, Position, {"id": "failed"})

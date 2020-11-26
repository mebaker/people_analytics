from unittest import TestCase
import pandas as pd
from ..employee import Employee


class EmployeeTest(TestCase):
    def test_init(self):
        data = pd.read_csv("./test/data/employee.csv", na_filter=False).to_dict(
            "records"
        )
        data = list(map(lambda x: Employee(x), data))
        self.assertTrue(isinstance(data[0], Employee))

    def test_failed_init(self):
        self.assertRaises(Exception, Employee, {"id": "failed"})

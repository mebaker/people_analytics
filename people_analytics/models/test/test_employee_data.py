from unittest import TestCase
import pandas as pd
from ..employee_data import EmployeeData

class EmployeeDataTest(TestCase):

    def test_init(self):
        data = pd.read_csv('./test/data/employee_data.csv', na_filter=False).to_dict('records')
        data = list(map(lambda x: EmployeeData(x), data))
        self.assertTrue(isinstance(data[0], EmployeeData))

    def test_failed_init(self):
        self.assertRaises(Exception, EmployeeData, { 'id': 'failed' })

from luigi import Task
import pandas as pd
from .utils import Requirement, Requires
from .load_employee import LoadEmployee
from .load_employee_data import LoadEmployeeData
from .load_position import LoadPosition


class CleanData(Task):

    requires = Requires()
    employee = Requirement(LoadEmployee)
    employeeData = Requirement(LoadEmployeeData)
    position = Requirement(LoadPosition)

    def run(self):
        employee = pd.read_pickle(self.input().get("employee").open("r"))
        employeeData = pd.read_pickle(self.input().get("employeeData").open("r"))
        position = pd.read_pickle(self.input().get("position").open("r"))

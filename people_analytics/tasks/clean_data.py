import pickle
from luigi import Task, LocalTarget, format
import pandas as pd
from .utils import Requirement, Requires
from .load_employee import LoadEmployee
from .load_employee_data import LoadEmployeeData
from .load_position import LoadPosition


class CleanData(Task):

    target = "./data/data.p"

    requires = Requires()
    employee = Requirement(LoadEmployee)
    employeeData = Requirement(LoadEmployeeData)
    position = Requirement(LoadPosition)

    def output(self):
        return LocalTarget(self.target, format=format.Nop)

    def run(self):
        employee = pd.read_pickle(self.input().get("employee").open("r"))
        employeeData = pd.read_pickle(self.input().get("employeeData").open("r"))
        position = pd.read_pickle(self.input().get("position").open("r"))
        data = pd.concat([employee, employeeData, position], axis=1)
        with self.output().temporary_path() as temp_output_path:
            with open(temp_output_path, "wb") as out:
                pickle.dump(data, out)

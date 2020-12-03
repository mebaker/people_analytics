import pickle
from luigi import Task, LocalTarget, format
import pandas as pd
from .utils import Requirement, Requires
from .load_employee import LoadEmployee
from .load_employee_data import LoadEmployeeData
from .load_position import LoadPosition
from .load_term import LoadTerm


class CleanData(Task):

    target = "./data/data.p"

    requires = Requires()
    employee = Requirement(LoadEmployee)
    employeeData = Requirement(LoadEmployeeData)
    position = Requirement(LoadPosition)
    term = Requirement(LoadTerm)

    def output(self):
        return LocalTarget(self.target, format=format.Nop)

    def run(self):
        employee = pd.read_pickle(self.input().get("employee").open("r"))
        employeeData = pd.read_pickle(self.input().get("employeeData").open("r"))
        position = pd.read_pickle(self.input().get("position").open("r"))
        term = pd.read_pickle(self.input().get("term").open("r"))
        data = pd.concat([employee, employeeData, position, term], axis=1)
        with self.output().temporary_path() as temp_output_path:
            with open(temp_output_path, "wb") as out:
                pickle.dump(data, out)

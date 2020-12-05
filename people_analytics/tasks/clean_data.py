import pickle
from luigi import Task, LocalTarget, format
import pandas as pd
from .utils import Requirement, Requires
from .load_employee import LoadEmployee
from .load_employee_data import LoadEmployeeData
from .load_position import LoadPosition
from .load_term import LoadTerm
from .load_comp import LoadComp

from ..models.position import ManagementLevel


class CleanData(Task):

    target = "./data/data.p"

    requires = Requires()
    employee = Requirement(LoadEmployee)
    employee_data = Requirement(LoadEmployeeData)
    position = Requirement(LoadPosition)
    term = Requirement(LoadTerm)
    comp = Requirement(LoadComp)

    def output(self):
        return LocalTarget(self.target, format=format.Nop)

    def run(self):
        employee = pd.read_pickle(self.input().get("employee").open("r"))
        employee_data = pd.read_pickle(self.input().get("employee_data").open("r"))
        position = pd.read_pickle(self.input().get("position").open("r"))
        term = pd.read_pickle(self.input().get("term").open("r"))
        comp = pd.read_pickle(self.input().get("comp").open("r"))
        data = pd.concat([employee, employee_data, position, term, comp], axis=1)
        data["is_manager"] = data["management_level"] < int(ManagementLevel.Principal)
        with self.output().temporary_path() as temp_output_path:
            with open(temp_output_path, "wb") as out:
                pickle.dump(data, out)

import pickle
from luigi import Task, LocalTarget, format, Parameter
import pandas as pd
from .utils import Requirement, Requires
from .load_employee import LoadEmployee
from .load_employee_data import LoadEmployeeData
from .load_position import LoadPosition
from .load_term import LoadTerm
from .load_comp import LoadComp
from datetime import datetime

from ..models.position import ManagementLevel


class CleanData(Task):
    report_date = Parameter(default=datetime.now().strftime("%m/%d/%Y"))

    requires = Requires()
    employee = Requirement(LoadEmployee)
    employee_data = Requirement(LoadEmployeeData)
    position = Requirement(LoadPosition)
    term = Requirement(LoadTerm)
    comp = Requirement(LoadComp)

    def output(self):
        target = "./data/temp/{}/data.p".format(self.report_date)
        return LocalTarget(target, format=format.Nop)

    def run(self):
        employee = pd.read_pickle(self.input().get("employee").open("r"))
        employee_data = pd.read_pickle(self.input().get("employee_data").open("r"))
        position = pd.read_pickle(self.input().get("position").open("r"))
        term = pd.read_pickle(self.input().get("term").open("r"))
        comp = pd.read_pickle(self.input().get("comp").open("r"))
        data = pd.concat([employee, employee_data, position, term, comp], axis=1)
        data["is_manager"] = (
            data["management_level"].apply(lambda ml: ml.value)
            < ManagementLevel.Principal.value
        )
        with self.output().temporary_path() as temp_output_path:
            with open(temp_output_path, "wb") as out:
                pickle.dump(data, out)

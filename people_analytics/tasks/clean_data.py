from luigi import Task
import pandas as pd
from .utils import Requirement, Requires
from .load_employee import LoadEmployee


class CleanData(Task):

    requires = Requires()
    employee = Requirement(LoadEmployee)

    def run(self):
        employee = pd.read_pickle(self.input().get('employee').open('r'))
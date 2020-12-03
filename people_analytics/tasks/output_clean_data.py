import pickle
from luigi import Task, LocalTarget, format
from .utils import Requirement, Requires
from .clean_data import CleanData

import pandas as pd


class OutputCleanData(Task):

    target = "./data/cleaned-data.csv"

    requires = Requires()
    data = Requirement(CleanData)

    def output(self):
        return LocalTarget(self.target, format=format.Nop)

    def run(self):
        data = pickle.load(self.input().get("data").open("r"))
        data["gender"] = data["gender"].apply(lambda gender: gender.name)
        data["management_level"] = data["management_level"].apply(
            lambda management_level: management_level.name
        )
        with self.output().temporary_path() as temp_output_path:
            data.to_csv(temp_output_path, compression=None, index_label="employee_id")

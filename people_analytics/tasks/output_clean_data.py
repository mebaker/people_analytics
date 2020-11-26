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
        data = pd.concat([data["employee"], data["position"]], axis=1)
        with self.output().temporary_path() as temp_output_path:
            data.to_csv(temp_output_path, compression=None)

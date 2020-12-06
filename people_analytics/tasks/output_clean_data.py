import pickle
from luigi import Task, LocalTarget, format, Parameter
from .utils import Requirement, Requires
from .clean_data import CleanData
from datetime import datetime


class OutputCleanData(Task):
    report_date = Parameter(default=datetime.now().strftime("%m/%d/%Y"))

    requires = Requires()
    data = Requirement(CleanData)

    def output(self):
        target = "./data/output/{}/cleaned-data.csv".format(self.report_date)
        return LocalTarget(target, format=format.Nop)

    def run(self):
        data = pickle.load(self.input().get("data").open("r"))
        data["gender"] = data["gender"].apply(lambda gender: gender.name)
        data["generation"] = data["generation"].apply(
            lambda generation: generation.name
        )
        data["management_level"] = data["management_level"].apply(
            lambda management_level: management_level.name
        )
        with self.output().temporary_path() as temp_output_path:
            data.to_csv(temp_output_path, compression=None, index_label="employee_id")

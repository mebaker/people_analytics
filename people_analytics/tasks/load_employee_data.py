from luigi import Task, LocalTarget, format
import pandas as pd

from ..models.employee_data import EmployeeData


class LoadEmployeeData(Task):

    file = "./data/employee_data.csv"
    target = str(file).replace(".csv", ".p")

    def output(self):
        return LocalTarget(self.target, format=format.Nop)

    def run(self):
        data = pd.read_csv(self.file, na_filter=False).to_dict("records")
        data = list(map(lambda x: EmployeeData(x).__dict__, data))
        data = pd.DataFrame.from_dict(data)
        with self.output().temporary_path() as temp_output_path:
            data.to_pickle(temp_output_path, compression=None)

from luigi import Task, LocalTarget, format, Parameter
import pandas as pd
from datetime import datetime

from ..models.employee import Employee


class LoadEmployee(Task):
    report_date = Parameter()
    file = "./data/input/employee.csv"

    def output(self):
        target = (
            str(self.file)
            .replace("input", "temp/{}".format(self.report_date))
            .replace(".csv", ".p")
        )
        return LocalTarget(target, format=format.Nop)

    def run(self):
        data = pd.read_csv(self.file, na_filter=False).to_dict("records")
        data = list(map(lambda x: Employee(x).__dict__, data))
        data = pd.DataFrame.from_dict(data)
        data.set_index("id", inplace=True)
        data.drop(["created_at"], axis=1, inplace=True)
        with self.output().temporary_path() as temp_output_path:
            data.to_pickle(temp_output_path, compression=None)

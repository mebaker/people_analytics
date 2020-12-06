from luigi import Task, LocalTarget, format, Parameter
import pandas as pd
from datetime import datetime

from ..models.employee_data import EmployeeData


class LoadEmployeeData(Task):
    report_date = Parameter(default=datetime.now().strftime("%m/%d/%Y"))
    file = "./data/input/employee_data.csv"

    def output(self):
        target = (
            str(self.file)
            .replace("input", "temp/{}".format(self.report_date))
            .replace(".csv", ".p")
        )
        return LocalTarget(target, format=format.Nop)

    def run(self):
        data = pd.read_csv(self.file, na_filter=False).to_dict("records")
        data = list(map(lambda x: EmployeeData(x).__dict__, data))
        data = pd.DataFrame.from_dict(data)
        data = data[data["created_at"] <= self.report_date]
        data.sort_values(by=["created_at"], inplace=True)
        data.drop_duplicates(subset=["employeeId"], keep="last", inplace=True)
        data.drop(["id"], axis=1, inplace=True)
        data.drop(["created_at"], axis=1, inplace=True)
        data.set_index("employeeId", inplace=True)
        with self.output().temporary_path() as temp_output_path:
            data.to_pickle(temp_output_path, compression=None)

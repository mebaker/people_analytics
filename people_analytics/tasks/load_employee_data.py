from luigi import Task, LocalTarget, format, Parameter
import pandas as pd
from datetime import datetime

from ..models.employee_data import EmployeeData


class LoadEmployeeData(Task):
    report_date = Parameter(default=datetime.now().strftime("%m/%d/%Y"))
    file = "./data/employee_data.csv"
    target = str(file).replace(".csv", ".p")

    def output(self):
        return LocalTarget(self.target, format=format.Nop)

    def run(self):
        data = pd.read_csv(self.file, na_filter=False).to_dict("records")
        data = list(map(lambda x: EmployeeData(x).__dict__, data))
        data = pd.DataFrame.from_dict(data)
        data = data[data["createdAt"] <= self.report_date]
        data.sort_values(by=["createdAt"], inplace=True)
        data.drop_duplicates(subset=["employeeId"], keep="last", inplace=True)
        data.drop(["id"], axis=1, inplace=True)
        data.drop(["createdAt"], axis=1, inplace=True)
        data.set_index("employeeId", inplace=True)
        with self.output().temporary_path() as temp_output_path:
            data.to_pickle(temp_output_path, compression=None)
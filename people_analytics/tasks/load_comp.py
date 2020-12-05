from luigi import Task, LocalTarget, format, Parameter
import pandas as pd
from datetime import datetime

from ..models.comp import Comp


class LoadComp(Task):
    report_date = Parameter(default=datetime.now().strftime("%m/%d/%Y"))
    file = "./data/input/comp.csv"
    target = str(file).replace("/input", "").replace(".csv", ".p")

    def output(self):
        return LocalTarget(self.target, format=format.Nop)

    def run(self):
        data = pd.read_csv(self.file, na_filter=False).to_dict("records")
        data = list(map(lambda x: Comp(x).__dict__, data))
        data = pd.DataFrame.from_dict(data)
        data.set_index("employee_id", inplace=True)
        data.drop(["created_at"], axis=1, inplace=True)
        with self.output().temporary_path() as temp_output_path:
            data.to_pickle(temp_output_path, compression=None)

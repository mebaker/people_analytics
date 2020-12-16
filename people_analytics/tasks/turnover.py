import pickle
import pandas as pd
from luigi import Task, LocalTarget, format, Parameter
from datetime import datetime
from .utils import Requirement, Requires
from .clean_data import CleanData
from ..metrics import cal_headcount

class Turnover(Task):
    report_date = Parameter(default=datetime.now().strftime("%m/%d/%Y"))

    requires = Requires()
    data = Requirement(CleanData)

    def output(self):
        target = "./data/output/{}/turnover.csv".format(self.report_date)
        return LocalTarget(target, format=format.Nop)

    def run(self):
        self.data = pickle.load(self.input().get("data").open("r"))
        terms = len(self.data[self.data['termination_date'].notnull()])
        headcount = cal_headcount(self.data)
        turnover_rate = (terms / headcount) * 100
        turn_df = pd.DataFrame.from_records({'Turnover Rate':[turnover_rate]})
        with self.output().temporary_path() as temp_output_path:
            turn_df.to_csv(temp_output_path, compression=None, index=False)

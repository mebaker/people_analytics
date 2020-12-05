import pickle
import pandas as pd
from luigi import Task, LocalTarget, format
from .utils import Requirement, Requires
from .clean_data import CleanData
from ..models.employee import Gender
from ..metrics import cal_headcount


class SiteMetrics(Task):

    target = "./data/site_metrics.csv"

    requires = Requires()
    data = Requirement(CleanData)

    def site_analysis(self, site):
        data: pd.DataFrame = self.data
        site_data = data[data["site"] == site]
        headcount = cal_headcount(site_data)
        female = cal_headcount(site_data[site_data["gender"] == Gender.FEMALE])
        male = cal_headcount(site_data[site_data["gender"] == Gender.MALE])
        return {
            "site": site,
            "headcount": headcount,
            "female": female,
            "female_ratio": female / headcount,
            "male": male,
            "male_ratio": male / headcount,
        }

    def output(self):
        return LocalTarget(self.target, format=format.Nop)

    def run(self):
        self.data = pickle.load(self.input().get("data").open("r"))
        sites = self.data["site"].unique()
        site_data = list(map(self.site_analysis, sites))
        site_data = pd.DataFrame.from_dict(site_data)
        with self.output().temporary_path() as temp_output_path:
            site_data.to_csv(temp_output_path, compression=None, index_label="site")

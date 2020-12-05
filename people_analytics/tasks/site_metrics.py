import pickle
import pandas as pd
from luigi import Task, LocalTarget, format
from .utils import Requirement, Requires
from .clean_data import CleanData
from ..models.employee import Gender
from ..metrics import cal_headcount
from ..models.position import ManagementLevel


class SiteMetrics(Task):

    target = "./data/output/site_analytics.csv"

    requires = Requires()
    data = Requirement(CleanData)

    def site_analysis(self, sites):
        data: pd.DataFrame = self.data
        levels = list(ManagementLevel)
        output = []
        for site in sites:
            site_data = data[data["site"] == site]
            for level in levels:
                site_level_data = site_data[site_data["management_level"] == level]
                if len(site_level_data) == 0:
                    continue
                headcount = cal_headcount(site_level_data)
                female = cal_headcount(
                    site_level_data[site_level_data["gender"] == Gender.FEMALE]
                )
                male = cal_headcount(
                    site_level_data[site_level_data["gender"] == Gender.MALE]
                )
                avg_base_salary = site_level_data["annual_comp_usd"].mean()
                avg_bonus = site_level_data["total_incentive_usd"].mean()
                output.append(
                    {
                        "site": site,
                        "level": level,
                        "headcount": headcount,
                        "female": female,
                        "female_ratio": female / headcount,
                        "male": male,
                        "male_ratio": male / headcount,
                        "avg_base_salary": avg_base_salary,
                        "avg_bonus": avg_bonus,
                    }
                )
        return output

    def output(self):
        return LocalTarget(self.target, format=format.Nop)

    def run(self):
        self.data = pickle.load(self.input().get("data").open("r"))
        sites = self.data["site"].unique()
        site_data = pd.DataFrame.from_dict(self.site_analysis(sites))
        site_data["level"] = site_data["level"].apply(lambda ml: ml.name)
        with self.output().temporary_path() as temp_output_path:
            site_data.to_csv(temp_output_path, compression=None, index_label="site")

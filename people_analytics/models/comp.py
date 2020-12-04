from schema import Schema, Use, Optional
from datetime import datetime, date
from dateutil.parser import parse

schema = Schema(
    {
        "employee_id": Use(str),
        "annual_comp_local": Use(float),
        "annual_comp_local_curr": str,
        "annual_comp_usd": Use(float),
        "total_incentive_local": Use(float),
        "total_incentive_usd": Use(float),
        "sale_effective_date": date,
        "incentive_effective_date": date,
        "fte": Use(float),
        "comp_ratio": Use(float),
        "salary_range_low": Use(float),
        "salary_range_midpoint": Use(float),
        "salary_range_high": Use(float),
        "grade": Use(str),
        Optional("created_at"): date,
    }
)


class Comp:
    def __init__(self, comp):
        comp["sale_effective_date"] = parse(comp["sale_effective_date"]).date()
        comp["incentive_effective_date"] = parse(
            comp["incentive_effective_date"]
        ).date()
        comp["created_at"] = (
            parse(comp["created_at"]) if comp["created_at"] else datetime.now().date()
        )
        if self.validate(comp):
            self.employee_id = comp["employee_id"]
            self.annual_comp_local = comp["annual_comp_local"]
            self.annual_comp_local_curr = comp["annual_comp_local_curr"]
            self.annual_comp_usd = comp["annual_comp_usd"]
            self.total_incentive_local = comp["total_incentive_local"]
            self.sale_effective_date = comp["sale_effective_date"]
            self.incentive_effective_date = comp["incentive_effective_date"]
            self.fte = comp["fte"]
            self.comp_ratio = comp["comp_ratio"]
            self.salary_range_low = comp["salary_range_low"]
            self.salary_range_midpoint = comp["salary_range_midpoint"]
            self.salary_range_high = comp["salary_range_high"]
            self.grade = comp["grade"]
            self.created_at = comp["created_at"]

    def validate(self, employee):
        return schema.validate(employee)

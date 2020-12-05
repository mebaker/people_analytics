from enum import IntEnum
from schema import Schema, Use, Optional
from datetime import datetime, date
from dateutil.parser import parse


class ManagementLevel(IntEnum):
    CEO = 1
    EVP = 2
    DVP_CVP = 3
    SVP = 4
    VP = 5
    Senior_Director = 6
    Director = 7
    Senior_Manager = 8
    Manager = 9
    Fellow = 10
    Supervisor = 11
    Principal = 12
    Senior = 13
    Specialist = 14
    Support_5 = 15
    Support_4 = 16
    Associate = 17
    Support_3 = 18
    Support_2 = 19
    Support_1 = 20
    Temporary = 21
    Unknown = 22


schema = Schema(
    {
        "position_id": Use(str),
        "employeeId": Use(str),
        "position_start": date,
        "job_profile": str,
        "business_title": str,
        "management_level": ManagementLevel,
        "job_function": str,
        "business_unit": str,
        "parent_department": str,
        "department_name": str,
        "site": str,
        "department_id": Use(str),
        "manager_id": Use(str),
        Optional("created_at"): date,
    }
)


class Position:
    def __init__(self, position):
        position["position_start"] = parse(position["position_start"]).date()
        position["management_level"] = ManagementLevel[position["management_level"]]
        position["created_at"] = (
            parse(position["created_at"])
            if position["created_at"]
            else datetime.now().date()
        )
        if self.validate(position):
            self.position_id = position["position_id"]
            self.employeeId = position["employeeId"]
            self.position_start = position["position_start"]
            self.business_title = position["business_title"]
            self.management_level = position["management_level"]
            self.job_function = position["job_function"]
            self.business_unit = position["business_unit"]
            self.parent_department = position["parent_department"]
            self.department_name = position["department_name"]
            self.department_id = position["department_id"]
            self.manager_id = position["manager_id"]
            self.created_at = position["created_at"]
            self.site = position["site"]

    def validate(self, position):
        return schema.validate(position)

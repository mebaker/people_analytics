from enum import Enum
from uuid import uuid4
from schema import Schema, Use, Optional
from datetime import datetime, date
from dateutil.parser import parse


class EducationLevel(Enum):
    SOME_HIGH_SCHOOL = 1
    HIGH_SCHOOL = 2
    SOME_COLLEGE = 3
    ASSOCIATE = 4
    BACHELOR = 5
    MASTERS = 6
    PHD = 7
    UNKNOWN = 8


schema = Schema(
    {
        Optional("id"): Use(str),
        "employeeId": Use(str),
        "recentHiredDate": datetime,
        "educationLevel": EducationLevel,
        Optional("createdAt"): date,
    }
)


class EmployeeData:
    def __init__(self, employeeData):
        employeeData["createdAt"] = (
            parse(employeeData["createdAt"])
            if employeeData["createdAt"]
            else datetime.now().date()
        )
        employeeData["recentHiredDate"] = parse(employeeData["recentHiredDate"]).date()
        employeeData["educationLevel"] = EducationLevel[employeeData["educationLevel"]]
        if self.validate:
            self.id = employeeData["id"] or uuid4()
            self.employeeId = employeeData["employeeId"]
            self.recentHiredDate = employeeData["recentHiredDate"]
            self.createdAt = employeeData["createdAt"]

    def validate(self, employeeData):
        return schema.validate(employeeData)

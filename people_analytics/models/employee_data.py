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
        "recent_hired_date": datetime,
        "educationLevel": EducationLevel,
        Optional("created_at"): date,
    }
)


class EmployeeData:
    def __init__(self, employee_data):
        employee_data["created_at"] = (
            parse(employee_data["created_at"])
            if employee_data["created_at"]
            else datetime.now().date()
        )
        employee_data["recent_hired_date"] = parse(
            employee_data["recent_hired_date"]
        ).date()
        employee_data["educationLevel"] = EducationLevel[
            employee_data["educationLevel"]
        ]
        if self.validate:
            self.id = employee_data["id"] or uuid4()
            self.employeeId = employee_data["employeeId"]
            self.recent_hired_date = employee_data["recent_hired_date"]
            self.created_at = employee_data["created_at"]

    def validate(self, employee_data):
        return schema.validate(employee_data)

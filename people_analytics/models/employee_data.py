from scheme import Scheme, Use, Optional
from datetime import datetime

schema = Schema({
    'employeeId': Use(str),
    'recentHiredDate': Use(datetime),
    'education_level': 'High School',
    Optional('createdAt'): Use(datetime),
})


class EmployeeData:

    def __init__(self, employeeData):
        if (self.validate):
            self.createdAt = employee.createdAt or datetime.now()

    def validate(self, employee) -> Bool:
        return schema.validate(employee)

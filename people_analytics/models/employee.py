from enum import Enum
from schema import Schema, Use, Optional
from datetime import datetime, date
from dateutil.parser import parse

class Gender(Enum):
    MALE = 1
    FEMALE = 2
    NOT_DISCLOSED = 3
    UNKNOWN = 4

schema = Schema({
    'id': Use(str),
    'hiredDate': date,
    'birthdate': date,
    'gender': Gender,
    Optional('createdAt'): datetime
})


class Employee:

    def __init__(self, employee):
        employee['hiredDate'] = parse(employee['hiredDate']).date()
        employee['birthdate'] = parse(employee['birthdate']).date()
        employee['gender'] = Gender[employee['gender']]
        employee['createdAt'] = parse(employee['createdAt']) if employee['createdAt'] else datetime.now()
        if (self.validate(employee)):
            self.id = employee['id']
            self.hiredDate = employee['hiredDate']
            self.birthdate = employee['birthdate']
            self.gender = employee['gender']
            self.createdAt = employee['createdAt']

    def validate(self, employee):
        return schema.validate(employee)

from enum import Enum
from schema import Schema, Use, Optional
from datetime import datetime, date
from dateutil.parser import parse


class Gender(Enum):
    MALE = 1
    FEMALE = 2
    NOT_DISCLOSED = 3
    UNKNOWN = 4


class Generation(Enum):
    SILENT = 1
    BABY_BOOMER = 2
    GEN_X = 3
    MILLENNIAL = 4
    GEN_Z = 5
    GEN_ALPHA = 6
    UNKNOWN = 7


schema = Schema(
    {
        "id": Use(str),
        "hired_date": date,
        "birthdate": date,
        "gender": Gender,
        "generation": Generation,
        Optional("created_at"): datetime,
    }
)


def get_generation(birthdate: date):
    year = birthdate.year
    if year <= 1928 & year <= 1945:
        return Generation.SILENT
    if year <= 1946 & year <= 1964:
        return Generation.BABY_BOOMER
    if year <= 1965 & year <= 1980:
        return Generation.GEN_X
    if year <= 1981 & year <= 1995:
        return Generation.MILLENNIAL
    if year <= 1996 & year <= 2012:
        return Generation.GEN_Z
    if year >= 2013:
        return Generation.GEN_ALPHA
    return Generation.UNKNOWN


class Employee:
    def __init__(self, employee):
        employee["hired_date"] = parse(employee["hired_date"]).date()
        employee["birthdate"] = parse(employee["birthdate"]).date()
        employee["gender"] = Gender[employee["gender"]]
        employee["generation"] = get_generation(employee["birthdate"])
        employee["created_at"] = (
            parse(employee["created_at"]) if employee["created_at"] else datetime.now()
        )
        if self.validate(employee):
            self.id = employee["id"]
            self.hired_date = employee["hired_date"]
            self.birthdate = employee["birthdate"]
            self.gender = employee["gender"]
            self.created_at = employee["created_at"]
            self.generation = employee["generation"]

    def validate(self, employee):
        return schema.validate(employee)

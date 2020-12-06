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
    }
)


def get_generation(birthdate: date):
    generation = Generation.UNKNOWN
    year = birthdate.year
    if year > 2013:
        generation = Generation.GEN_ALPHA
    elif year > 1996:
        generation = Generation.GEN_Z
    elif year > 1981:
        generation = Generation.MILLENNIAL
    elif year > 1965:
        generation = Generation.GEN_X
    elif year > 1946:
        generation = Generation.BABY_BOOMER
    elif year > 1928:
        generation = Generation.SILENT
    return generation


class Employee:
    def __init__(self, employee):
        employee["hired_date"] = parse(employee["hired_date"]).date()
        employee["birthdate"] = parse(employee["birthdate"]).date()
        employee["gender"] = Gender[employee["gender"]]
        employee["generation"] = get_generation(employee["birthdate"])
        if self.validate(employee):
            self.id = employee["id"]
            self.hired_date = employee["hired_date"]
            self.birthdate = employee["birthdate"]
            self.gender = employee["gender"]
            self.generation = employee["generation"]

    def validate(self, employee):
        return schema.validate(employee)

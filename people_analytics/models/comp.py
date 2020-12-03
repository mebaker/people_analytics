from enum import Enum
from schema import Schema, Use, Optional
from datetime import datetime, date
from dateutil.parser import parse

schema = Schema({
    'id': Use(str),
    'annual_comp_local': float,
    'annual_comp_local_curr': str,
    'annual_comp_usd': float,
    'total_incentive_local': float,
    'total_incentive_usd': float,
    'sale_effective_date': date,
    'incentive_effective_date': date,
    'fte': float,
    'comp_ratio': float,
    'salary_range_low': float,
    'salary_range_midpoint': float,
    'salary_range_high': float,
    'grade': str,
    Optional('createdAt'): datetime
})


class Position:

    def __init__(self, position):
        position['position_start'] = parse(position['position_start']).date()
        position['management_level'] = ManagementLevel[position['management_level']]
        position['createdAt'] = parse(position['createdAt']) if position['createdAt'] else datetime.now()
        if (self.validate(position)):
            self.id = position['id']
            self.annual_comp_local = position['annual_comp_local']
            self.annual_comp_local_curr = position['annual_comp_local_curr']
            self.annual_comp_usd = position['annual_comp_usd']
            self.total_incentive_local = position['total_incentive_local']
            self.total_incentive_usd = position['total_incentive_usd']
            self.sale_effective_date = position['sale_effective_date']
            self.incentive_effective_date = position['incentive_effective_date']
            self.fte = position['fte']
            self.comp_ratio = position['comp_ratio']
            self.salary_range_low = position['salary_range_low']
            self.salary_range_midpoint = position['salary_range_midpoint']
            self.salary_range_high = position['salary_range_high']
            self.grade = position['grade']

    def validate(self, employee):
        return schema.validate(employee)
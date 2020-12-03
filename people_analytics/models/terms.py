from enum import Enum
from schema import Schema, Use, Optional
from datetime import datetime, date
from dateutil.parser import parse

schema = Schema({
    'id': Use(str),
    'termination_date': date,
    'last_date_worked': date,
    'term_type': str,
    'term_reason': str,
    Optional('createdAt'): datetime
})


class Position:

    def __init__(self, position):
        position['position_start'] = parse(position['position_start']).date()
        position['management_level'] = ManagementLevel[position['management_level']]
        position['createdAt'] = parse(position['createdAt']) if position['createdAt'] else datetime.now()
        if (self.validate(position)):
            self.id = position['id']
            self.termination_date = position['termination_date']
            self.last_date_worked = position['last_date_worked']
            self.term_type = position['term_type']
            self.term_reason = position['term_reason']

    def validate(self, employee):
        return schema.validate(employee)
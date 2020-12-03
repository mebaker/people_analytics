from schema import Schema, Use, Optional
from datetime import datetime, date
from dateutil.parser import parse

schema = Schema(
    {
        "employee_id": Use(str),
        "termination_date": date,
        "last_date_worked": date,
        "term_type": str,
        "term_reason": str,
        Optional("created_at"): date,
    }
)


class Term:
    def __init__(self, term):
        term["termination_date"] = parse(term["termination_date"])
        term["last_date_worked"] = parse(term["last_date_worked"])
        term["created_at"] = (
            parse(term["created_at"]) if term["created_at"] else datetime.now().date()
        )
        if self.validate(term):
            self.employee_id = term["employee_id"]
            self.termination_date = term["termination_date"]
            self.last_date_worked = term["last_date_worked"]
            self.term_type = term["term_type"]
            self.term_reason = term["term_reason"]
            self.created_at = term["created_at"]

    def validate(self, term):
        return schema.validate(term)

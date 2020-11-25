from scheme import Scheme

schema = Schema({
    'employeeId': Use(str)
})


class Employee:

    def __init__(self, employee):
        if (self.validate):
            self.employeeId = employee.employeeId

    def validate(self, employee) -> Bool:
        return schema.validate(employee)

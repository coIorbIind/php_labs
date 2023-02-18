from typing import List

from pydantic import BaseModel

from .employee import EmployeeSchema


class DepartmentSchema(BaseModel):
    id: int
    name: str
    employees: List[EmployeeSchema]

    def total_salary(self) -> int:
        return sum([employee.salary for employee in self.employees])

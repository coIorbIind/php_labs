from datetime import date
from dateutil.relativedelta import relativedelta

from pydantic import BaseModel, validator


class EmployeeSchema(BaseModel):
    id: int
    name: str
    salary: int
    employment_date: date

    def experience(self) -> int:
        return relativedelta(date.today(), self.employment_date).years

    @validator('name')
    def name_validator(cls, v):
        if not str.isalpha(v):
            raise ValueError('Name should contains only letters')
        return v.title()

    @validator('employment_date')
    def employment_date_validator(cls, v):
        if v > date.today():
            raise ValueError('Future employment date')
        return v

    @validator('salary')
    def salary_validator(cls, v):
        if v <= 0:
            raise ValueError('I want to make more!')
        return v

import pytest
from datetime import date

from api.schemas.employee import EmployeeSchema
from api.schemas.department import DepartmentSchema


def test_departments_sorting():
    emp1 = EmployeeSchema(id=1, name='name', salary=5, employment_date=date.today())
    emp2 = EmployeeSchema(id=2, name='name', salary=5, employment_date=date.today())
    emp3 = EmployeeSchema(id=3, name='name', salary=10, employment_date=date.today())
    emp4 = EmployeeSchema(id=4, name='name', salary=1, employment_date=date.today())
    emp5 = EmployeeSchema(id=5, name='name', salary=1, employment_date=date.today())

    departments = [
        DepartmentSchema(id=1, name='rich', employees=[emp1, emp2]),
        DepartmentSchema(id=2, name='notrich', employees=[emp3]),

        DepartmentSchema(id=3, name='first_poor', employees=[emp4]),
        DepartmentSchema(id=4, name='second_poor', employees=[emp5])
    ]

    salary_employees = dict()
    for dep in departments:
        total_salary = dep.total_salary()
        if total_salary in salary_employees:
            if len(salary_employees[total_salary][0].employees) < len(dep.employees):
                salary_employees[total_salary] = [dep]
            elif len(salary_employees[total_salary][0].employees) == len(dep.employees):
                salary_employees[total_salary].append(dep)
        else:
            salary_employees[total_salary] = [dep]

    max_deps = salary_employees[max(salary_employees)]
    min_deps = salary_employees[min(salary_employees)]

    assert len(max_deps) == 1
    assert max_deps[0].name == 'rich'

    assert len(min_deps) == 2
    assert {dep.name for dep in min_deps} == {'first_poor', 'second_poor'}


def test_total_salary():
    emp1 = EmployeeSchema(id=1, name='name', salary=5, employment_date=date.today())
    emp2 = EmployeeSchema(id=2, name='name', salary=5, employment_date=date.today())

    department = DepartmentSchema(id=1, name='rich', employees=[emp1, emp2])

    assert department.total_salary() == 10

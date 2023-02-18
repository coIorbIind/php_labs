import pytest
from freezegun import freeze_time

from datetime import date, timedelta

from pydantic.error_wrappers import ValidationError

from api.schemas.employee import EmployeeSchema


@freeze_time('2023-01-01')
@pytest.mark.parametrize(
    'employment_date', [date(year=2022, month=1, day=1), date(year=2022, month=1, day=5)]
)
def test_employment_date(employment_date):
    emp = EmployeeSchema(id=1, name='name', salary=5, employment_date=employment_date)
    if employment_date.day == 5:
        assert emp.experience() == 0
    else:
        assert emp.experience() == 1


@pytest.mark.parametrize(
    'kwargs',
    [
        {'id': 'sd', 'name': 'name', 'salary': 5, 'employment_date': date.today()},
        {'id': 1, 'name': 'name1', 'salary': 5, 'employment_date': date.today()},
        {'id': 1, 'name': 'name', 'salary': -1, 'employment_date': date.today()},
        {'id': 1, 'name': 'name', 'salary': 5, 'employment_date': date.today() + timedelta(days=6)},
    ]
)
def test_incorrect_data(kwargs):
    with pytest.raises(ValidationError):
        EmployeeSchema(**kwargs)

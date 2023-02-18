from fastapi import APIRouter

from api.routers.employee import router as employee_router
from api.routers.department import router as department_router


api_router = APIRouter()
api_router.include_router(employee_router, prefix='', tags=['employee'])
api_router.include_router(department_router, prefix='', tags=['department'])

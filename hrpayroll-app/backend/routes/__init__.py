from fastapi import APIRouter
from .auth import router as auth_router
from .employees import router as employees_router
from .payroll import router as payroll_router
from .departments import router as departments_router

# Create main router for all API routes
api_router = APIRouter()

# Include all routers
api_router.include_router(auth_router)
api_router.include_router(employees_router)
api_router.include_router(payroll_router)
api_router.include_router(departments_router)

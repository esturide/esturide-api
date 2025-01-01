from fastapi import APIRouter, Depends
from app.application.uses_cases.automobile import AutomobileUseCase
from app.presentation.schemes import AutomobileRequest, AutomobileResponse

automobile_router = APIRouter(
    prefix="/automobile",
    tags=["Automobile Management"],
)

def get_automobile_use_case() -> AutomobileUseCase:
    return AutomobileUseCase()

@automobile_router.get("/{code}", response_model=AutomobileResponse)
async def get_automobile(code: int, use_case: AutomobileUseCase = Depends(get_automobile_use_case)):
    return await use_case.get(code)

@automobile_router.post("/", response_model=AutomobileResponse)
async def create_automobile(automobile_request: AutomobileRequest, use_case: AutomobileUseCase = Depends(get_automobile_use_case)):
    return await use_case.create(automobile_request)

@automobile_router.put("/{code}", response_model=AutomobileResponse)
async def update_automobile(code: int, automobile_request: AutomobileRequest, use_case: AutomobileUseCase = Depends(get_automobile_use_case)):
    return await use_case.update(code, automobile_request)

@automobile_router.delete("/{code}")
async def delete_automobile(code: int, use_case: AutomobileUseCase = Depends(get_automobile_use_case)):
    return await use_case.delete(code)

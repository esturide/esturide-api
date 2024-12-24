from fastapi import APIRouter, HTTPException, Depends
from app.application.uses_cases.auth_travel import authenticate_trip
from app.presentation.schemes import AuthTravelRequest

auth_travel = APIRouter(prefix="/auth", tags=["Auth Travel"])

@auth_travel.get('/')
async def index():
    return {
        "status": "ok",
    }


@auth_travel.post("/authenticate_travel")
async def authenticate_travel(request: AuthTravelRequest, auth = Depends(authenticate_trip)):
    try:
        result = await auth(user_id=request.user_id, trip_id=request.trip_id)

        return {
            "status": "success",
            "message": "Authorized" if result else "Unauthorized"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

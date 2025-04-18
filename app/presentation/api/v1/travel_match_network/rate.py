from fastapi import APIRouter, HTTPException, Depends

from app.application.uses_cases.rate import rate_trip
from app.presentation.schemes import RateRequest

rate = APIRouter(prefix="/rate", tags=["Rating"])


@rate.post("/rate_trip")
async def rate_travel(request: RateRequest, rate=Depends(rate_trip)):
    try:
        await rate(
            user_id=request.user_id,
            schedule_id=request.schedule_id,
            overall=request.overall,
            punctuality=request.punctuality,
            driving_behavior=request.driving_behavior
        )

        return {"status": "success", "message": "Rating submited successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error ocurred")

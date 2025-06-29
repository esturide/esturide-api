from datetime import time
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Query
from neomodel.exceptions import DoesNotExist

from app.core.dependencies import DependScheduleCase, AuthUserCredentials
from app.core.types import UUID
from app.domain.models import Schedule
from app.presentation.schemes import DriverProfile, ScheduleTravel, TravelResult

travel = APIRouter(prefix="/travel", tags=["Travels"])


@travel.get("/search")
async def search_travel(schedule_case: DependScheduleCase, auth_user: AuthUserCredentials, limit: int = 16):
    return await schedule_case.get_all_travels(limit)


@travel.get("/")
async def get_all_travels(schedule_case: DependScheduleCase, auth_user: AuthUserCredentials, limit: int = 16):
    return await schedule_case.get_all_travels(limit)


@travel.post("/")
async def schedule_new_travel(schedule: ScheduleTravel, schedule_case: DependScheduleCase,
                              auth_user: AuthUserCredentials):
    status = await schedule_case.create(schedule, auth_user)

    if not status:
        raise HTTPException(status_code=400)

    return {
        "status": "success",
    }


@travel.get("/{uuid}")
async def get_travel(uuid: UUID, schedule_case: DependScheduleCase, auth_user: AuthUserCredentials):
    return await schedule_case.get(uuid, auth_user)


@travel.delete("/cancel/{uuid}")
async def cancel_travel(uuid: UUID, schedule_case: DependScheduleCase, auth_user: AuthUserCredentials):
    status = await schedule_case.cancel(uuid, auth_user)

    return {
        "status": "success" if status else "failure",
    }


@travel.get(
    "/search",
    response_model=List[TravelResult],
    summary="Buscar viajes con filtros y ordenamiento"
)
async def search_schedule(
        schedule_case: DependScheduleCase,
        auth_user: AuthUserCredentials,
        start_time_from: Optional[time] = Query(None, alias="start_time_from"),
        start_time_to: Optional[time] = Query(None, alias="start_time_to"),
        end_time_from: Optional[time] = Query(None, alias="end_time_from"),
        end_time_to: Optional[time] = Query(None, alias="end_time_to"),
        minimum_price: Optional[int] = Query(None, alias="minimum_price"),
        maximum_price: Optional[int] = Query(None, alias="maximum_price"),
        min_passengers: Optional[int] = Query(None, alias="min_passengers"),
        max_passengers: Optional[int] = Query(None, alias="max_passengers"),
        driver_gender: Optional[str] = Query(None, alias="driver_gender"),
        sort: Optional[str] = Query(
            None,
            alias="sort",
            description="Opciones: start-time, end-time, minimum-price, maximum-price"
        )
):
    return await schedule_case.search(
        user=auth_user,
        start_time_from=start_time_from,
        start_time_to=start_time_to,
        end_time_from=end_time_from,
        end_time_to=end_time_to,
        minimum_price=minimum_price,
        maximum_price=maximum_price,
        min_passengers=min_passengers,
        max_passengers=max_passengers,
        driver_gender=driver_gender,
        sort=sort,
    )


@travel.get(
    "/all",
    response_model=List[TravelResult],
    summary="Obtener todos los viajes con filtros avanzados"
)
async def get_all_schedules(
        schedule_case: DependScheduleCase,
        auth_user: AuthUserCredentials,
        start_time_from: Optional[time] = Query(None, alias="start_time_from"),
        start_time_to: Optional[time] = Query(None, alias="start_time_to"),
        end_time_from: Optional[time] = Query(None, alias="end_time_from"),
        end_time_to: Optional[time] = Query(None, alias="end_time_to"),
        minimum_price: Optional[int] = Query(None, alias="minimum_price"),
        maximum_price: Optional[int] = Query(None, alias="maximum_price"),
        min_passengers: Optional[int] = Query(None, alias="min_passengers"),
        max_passengers: Optional[int] = Query(None, alias="max_passengers"),
        driver_gender: Optional[str] = Query(None, alias="driver_gender"),
        active: Optional[bool] = Query(None, description="True para solo activos"),
        terminated: Optional[bool] = Query(None, description="True para solo terminados"),
        canceled: Optional[bool] = Query(None, description="True para solo cancelados"),
        driver_code: Optional[int] = Query(None, alias="driver_code"),
):
    return await schedule_case.search(
        user=auth_user,
        start_time_from=start_time_from,
        start_time_to=start_time_to,
        end_time_from=end_time_from,
        end_time_to=end_time_to,
        minimum_price=minimum_price,
        maximum_price=maximum_price,
        min_passengers=min_passengers,
        max_passengers=max_passengers,
        driver_gender=driver_gender,
        active=active,
        terminated=terminated,
        canceled=canceled,
        driver_code=driver_code,
    )


@travel.get(
    "/status/{uuid}",
    summary="Obtener estado de un viaje: siempre driver; si eres conductor, también pasajeros"
)
async def get_schedule_status(
        uuid: UUID,
        auth_user: AuthUserCredentials,
):
    try:
        schedule = await Schedule.nodes.get(uuid=uuid)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Schedule not found")

    driver_node = await schedule.driver.single()
    driver = DriverProfile(
        code=driver_node.code,
        firstname=driver_node.firstname,
        maternal_surname=driver_node.maternal_surname,
        paternal_surname=driver_node.paternal_surname,
    )

    if auth_user.code == driver_node.code:
        raw_passengers = await schedule.passengers.all()
        passengers: List[DriverProfile] = [
            DriverProfile(
                code=p.code,
                firstname=p.firstname,
                maternal_surname=p.maternal_surname,
                paternal_surname=p.paternal_surname,
            )
            for p in raw_passengers
        ]
        return {"driver": driver, "passengers": passengers}

    return {"driver": driver}


@travel.patch(
    "/modification/{uuid}",
    summary="Modificar flags de un schedule: start, finished, cancel"
)
async def modify_schedule(
        schedule_case: DependScheduleCase,
        auth_user: AuthUserCredentials,
        uuid: UUID,
        start: Optional[bool] = Query(None, description="True para activar/inactivar el viaje"),
        finished: Optional[bool] = Query(None, description="True para marcar el viaje como terminado"),
        cancel: Optional[bool] = Query(None, description="True para cancelar el viaje"),
):
    try:
        updated_status = await schedule_case.modify(
            uuid=uuid,
            user=auth_user,
            start=start,
            finished=finished,
            cancel=cancel,
        )
    except HTTPException:
        raise
    return updated_status

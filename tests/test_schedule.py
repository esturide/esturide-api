import pytest
from app.application.uses_cases.schedule import ScheduleCase
from tests.factories.schedule_factory import create_schedule_factory, create_user_factory
from app.core.types import UUID
from app.domain.models import Schedule
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_create_schedule_with_valid_data():
    driver = await create_user_factory(role="D")
    schedule_case = ScheduleCase()
    schedule_data = await create_schedule_factory()

    schedule = await schedule_case.create(schedule_data, driver)

    assert schedule is not None
    assert schedule.max_passenger == schedule_data["max_passenger"]
    assert schedule.price == schedule_data["price"]


@pytest.mark.asyncio
async def test_create_schedule_with_invalid_data():
    driver = await create_user_factory(role="D")
    schedule_case = ScheduleCase()

    # Missing required fields
    schedule_data = {
        "max_passenger": None,
        "price": 100,
    }

    with pytest.raises(HTTPException) as excinfo:
        await schedule_case.create(schedule_data, driver)

    assert excinfo.value.status_code == 400


@pytest.mark.asyncio
async def test_get_schedule_success():
    schedule = await create_schedule_factory()
    schedule_case = ScheduleCase()

    fetched_schedule = await schedule_case.get(schedule.uuid, auth_user=schedule.driver)

    assert fetched_schedule.uuid == schedule.uuid


@pytest.mark.asyncio
async def test_get_schedule_unauthorized():
    schedule = await create_schedule_factory()
    another_user = await create_user_factory()

    schedule_case = ScheduleCase()

    with pytest.raises(HTTPException) as excinfo:
        await schedule_case.get(schedule.uuid, auth_user=another_user)

    assert excinfo.value.status_code == 401


@pytest.mark.asyncio
async def test_update_schedule_active_status():
    schedule = await create_schedule_factory()
    schedule_case = ScheduleCase()

    updated_status = await schedule_case.cancel(schedule.uuid, auth_user=schedule.driver)

    assert updated_status is True

    # Fetch again to confirm state
    _, updated_schedule = await schedule_case.get(schedule.uuid, auth_user=schedule.driver)
    assert updated_schedule.cancel is True


@pytest.mark.asyncio
async def test_delete_schedule():
    schedule = await create_schedule_factory()

    await schedule.delete()

    assert await Schedule.nodes.get_or_none(uuid=schedule.uuid) is None


@pytest.mark.asyncio
async def test_edge_cases():
    # Case 1: Trying to cancel an already cancelled schedule
    schedule = await create_schedule_factory()
    schedule_case = ScheduleCase()

    await schedule_case.cancel(schedule.uuid, auth_user=schedule.driver)
    with pytest.raises(HTTPException) as excinfo:
        await schedule_case.cancel(schedule.uuid, auth_user=schedule.driver)

    assert excinfo.value.status_code == 400

    # Case 2: Trying to create a schedule while having an active one
    driver = await create_user_factory(role="D")
    await create_schedule_factory(driver=driver)

    schedule_case = ScheduleCase()
    schedule_data = {
        "max_passenger": 4,
        "price": 150,
        "start": {
            "location": "City A",
            "latitude": "12.34",
            "longitude": "56.78",
        },
        "end": {
            "location": "City B",
            "latitude": "23.45",
            "longitude": "67.89",
        },
    }

    with pytest.raises(HTTPException) as excinfo:
        await schedule_case.create(schedule_data, driver)

    assert excinfo.value.status_code == 400

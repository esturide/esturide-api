from faker import Faker
from app.domain.models import Schedule, User
import random

from app.domain.types import LocationData

fake = Faker()

async def create_user_factory(role="S"):
    user = await User(
        firstname=fake.first_name(),
        paternal_surname=fake.last_name(),
        maternal_surname=fake.last_name(),
        code=fake.random_int(min=1000, max=9999),
        role=role,
        birth_date=fake.date_of_birth(),
        email=fake.email(),
        password=fake.password(),
        curp=fake.curp(),
    ).save()
    return user

async def create_record_factory():
    record = LocationData(
        latitude=random.uniform(0, 1),
        longitude=random.uniform(0, 1),
    )

    return record


async def create_schedule_factory(driver=None):
    if not driver:
        driver = await create_user_factory(role="D")

    start = await create_record_factory()
    finished = await create_record_factory()

    schedule = await Schedule(
        max_passenger=random.randint(1, 4),
        price=random.randint(10, 100),
        active=random.choice([True, False]),
        terminate=random.choice([True, False]),
        cancel=random.choice([True, False]),
        start=start,
        finish=finished,
    ).save()

    await driver.schedules.connect(schedule)

    return schedule

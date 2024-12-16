from faker import Faker
from app.domain.models import Schedule, Record, User
import random

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
    record = await Record(
        location=fake.city(),
        latitude=str(fake.latitude()),
        longitude=str(fake.longitude()),
    ).save()
    return record


async def create_schedule_factory(driver=None):
    if not driver:
        driver = await create_user_factory(role="D")

    origin = await create_record_factory()
    destination = await create_record_factory()

    schedule = await Schedule(
        max_passenger=random.randint(1, 4),
        price=random.randint(10, 100),
        active=random.choice([True, False]),
        terminate=random.choice([True, False]),
        cancel=random.choice([True, False]),
    ).save()

    await schedule.origin.connect(origin)
    await schedule.destination.connect(destination)
    await driver.schedules.connect(schedule)

    return schedule

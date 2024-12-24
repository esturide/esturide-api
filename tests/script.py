import asyncio
from .factories.schedule_factory import create_schedule_factory

async def generate_test_schedule():
    for _ in range(5):
        schedule = await create_schedule_factory()
        print(f"Generated Schedule: {schedule.uuid}")
        

asyncio.run(generate_test_schedule())

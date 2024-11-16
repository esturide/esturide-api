import random

from faker import Faker


def random_user_code():
    return random.randint(100000001, 9999999999)


def create_dummy_user_data() -> dict:
    faker = Faker('es_MX')

    return dict(
        code=random_user_code(),
        firstname=faker.name(),
        maternal_surname=faker.last_name(),
        paternal_surname=faker.last_name(),
        birth_date=faker.date_of_birth().strftime('%Y-%m-%d'),
        email=faker.email(),
        password=faker.password(),
        curp=faker.curp(),
    )

import random

from faker import Faker


def random_user_student_code() -> int:
    return random.randint(100000001, 9999999999)


def create_dummy_user_data(locale: str = 'es_MX') -> dict:
    faker = Faker(locale)

    return dict(
        code=random_user_student_code(),
        firstname=faker.name(),
        maternal_surname=faker.last_name(),
        paternal_surname=faker.last_name(),
        birth_date=faker.date_of_birth().strftime('%Y-%m-%d'),
        email=faker.email(),
        password=faker.password(),
        curp=faker.curp(),
    )

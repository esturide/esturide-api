import random

from faker import Faker


def random_user_student_code() -> int:
    return random.randint(100000001, 9999999999)


def faker_birth_date(faker, **kwargs):
    return str(faker.date_of_birth(**kwargs))


def create_dummy_user_data(locale: str = 'es_MX') -> dict:
    faker = Faker(locale)

    return dict(
        code=random_user_student_code(),
        firstname=faker.first_name(),
        maternal_surname=faker.last_name(),
        paternal_surname=faker.last_name(),
        birth_date=faker_birth_date(faker, minimum_age=18, maximum_age=90),
        email=faker.email(),
        password=faker.password(),
        curp=faker.curp(),
    )

from faker import Faker


def create_user(fake: Faker):
    return {
        "firstname": fake.first_name(),
        "paternalSurname": fake.last_name(),
        "maternalSurname": fake.last_name(),
        "code": fake.random_int(min=1000, max=79999999),
        "birth_date": fake.date_of_birth(minimum_age=18),
        "email": fake.email(),
        "password": fake.password(),
        "curp": fake.curp(),
    }

import pytest
from pydantic import ValidationError
from app.presentation.schemes import (TrackingRecord, RideRequest)
from faker import Faker
from uuid import UUID, uuid4
from app.presentation.schemes.travels import (
    DriverUser,
    PassengerUser,
    ScheduleTravelRequest,
    TravelScheduleResponse,
    Tracking,
)
from app.presentation.schemes.status import PassengerRideStatus
from app.core.utils.scheme_json import create_travel_scheme


faker = Faker()

@pytest.fixture
def tracking_record_data(faker):
    return {
        "latitude": faker.latitude(),
        "longitude": faker.longitude()
    }

def test_valid_tracking_record_creation(faker):
    """Test creating valid TrackingRecord without location"""
    data = {
        "latitude": faker.latitude(),
        "longitude": faker.longitude()
    }

    record = TrackingRecord()
    record.latitude = data["latitude"]
    record.longitude = data["longitude"]
    assert record.latitude == data["latitude"]
    assert record.latitude == data["latitude"]


def test_ride_request_schema(tracking_record_data):
    """Test RideRequest with valid TrackingRecord"""
    data = {
        "origin": tracking_record_data,
        "UUID": uuid4()
    }
    request = RideRequest(**data)
    assert isinstance(request.origin.latitude, float)
    assert isinstance(request.origin.longitude, float)


def test_driver_user_schema(tracking_record_data):
    """Test DriverUser schema without location in position"""
    data = {
        "code": "12345678",
        "firstname": faker.first_name(),
        "maternalSurname": faker.last_name(),
        "paternalSurname": faker.last_name(),
        "position": tracking_record_data
    }
    user = DriverUser(**data)
    assert isinstance(user.position.latitude, float)
    assert isinstance(user.position.longitude, float)

def test_travel_schedule_response_schema(tracking_record_data):
    """Test TravelScheduleResponse schema with valid TrackingRecords"""
    data = {
        "uuid": uuid4(),
        "price": 100,
        "driver": {
            "code": "12345678",
            "firstname": faker.first_name(),
            "maternalSurname": faker.last_name(),
            "paternalSurname": faker.last_name(),
            "position": tracking_record_data
        },
        "origin": tracking_record_data,
        "destination": tracking_record_data
    }
    response = TravelScheduleResponse(**data)
    assert isinstance(response.origin.latitude, float)
    assert isinstance(response.destination.longitude, float)


def test_create_travel_scheme(faker):
    """Test utility function creates valid TrackingRecords without location"""
    # Create dummy data
    class MockSchedule:
        uuid = uuid4()
        price = 100
        active = True
        terminate = False
        cancel = False
        max_passenger = 4

    class MockUser:
        code = "12345678"
        firstname = faker.first_name()
        maternal_surname = faker.last_name()
        paternal_surname = faker.last_name()

    class MockLocation:
        latitude = faker.latitude()
        longitude = faker.longitude()

    # Execute
    result = create_travel_scheme(
        schedule=MockSchedule(),
        driver=MockUser(),
        origin=MockLocation(),
        destination=MockLocation()
    )

    # Validate
    assert isinstance(result, TravelScheduleResponse)
    assert isinstance(result.origin, TrackingRecord)
    assert isinstance(result.destination, TrackingRecord)
    assert not hasattr(result.origin, "location")
    assert not hasattr(result.destination, "location")

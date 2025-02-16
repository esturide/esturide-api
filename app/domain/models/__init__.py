from typing import Tuple

from neomodel import AsyncStructuredNode, UniqueIdProperty, StringProperty, DateProperty, EmailProperty, \
    BooleanProperty, IntegerProperty, DateTimeProperty, AsyncStructuredRel, \
    AsyncRelationshipTo, AsyncRelationshipFrom, AsyncOne, AsyncZeroOrOne, JSONProperty, ArrayProperty

from app.core.encrypt import check_same_password
from app.core.enum import RoleUser
from app.domain.types import LocationData


class RecordTrackingMixin:
    uuid = UniqueIdProperty(indexed=True)
    record = ArrayProperty(JSONProperty())


class Ride(AsyncStructuredRel, RecordTrackingMixin):
    time = DateTimeProperty(default_now=True)
    validate = BooleanProperty(default=False)
    cancel = BooleanProperty(default=False)
    on_board = BooleanProperty(default=False)


class Travel(AsyncStructuredRel, RecordTrackingMixin):
    time = DateTimeProperty(default_now=True)


class User(AsyncStructuredNode):
    ROLES = {
        'P': 'passenger',
        'D': 'driver',
        'N': 'not-verified',
        'S': 'staff',
        'A': 'admin'
    }

    code = IntegerProperty(required=True, unique_index=True)
    hashed_password = StringProperty(required=True)
    salt = StringProperty(required=True)

    """General information"""
    firstname = StringProperty(required=True)
    maternal_surname = StringProperty(required=True)
    paternal_surname = StringProperty(required=True)
    birth_date = DateProperty(required=True)

    """Sensitive data"""
    email = EmailProperty(required=True, unique_index=True)
    curp = StringProperty(required=True)
    phone_number = StringProperty()

    valid_user = BooleanProperty(required=False, default=False)

    role = StringProperty(choices=ROLES, default='N')

    cars = AsyncRelationshipTo('Automobile', 'OWNS')

    rides = AsyncRelationshipTo("Schedule", 'RIDE_TO', model=Ride)
    schedules = AsyncRelationshipTo("Schedule", 'DRIVER_TO', model=Travel)

    def same_password(self, password: str):
        return check_same_password(
            password,
            self.hashed_password
        )

    @property
    def is_admin(self):
        return self.role == 'A'

    @property
    def is_staff(self):
        return self.role == 'S'

    @property
    def is_driver(self):
        return self.role == 'D'

    @property
    def is_passenger(self):
        return self.role == 'P'

    @property
    def is_validate(self):
        return self.valid_user

    @property
    def role_value(self):
        try:
            return RoleUser[User.ROLES[self.role]]
        except KeyError:
            return RoleUser.not_verified

    @role_value.setter
    def role_value(self, role: RoleUser):
        self.role = role.value.upper()[0]


class Automobile(AsyncStructuredNode):
    code = IntegerProperty(indexed=True, unique_index=True)
    brand = StringProperty(required=True, unique_index=True)
    year = IntegerProperty(required=True)
    model = StringProperty(required=True)

    schedule = AsyncRelationshipTo('Schedule', 'DRIVE')

    car = AsyncRelationshipFrom('User', 'OWNS')


class Schedule(AsyncStructuredNode):
    uuid = UniqueIdProperty(indexed=True)

    active = BooleanProperty(required=False, default=False)
    terminate = BooleanProperty(required=False, default=False)
    cancel = BooleanProperty(required=False, default=False)

    price = IntegerProperty(required=True)
    max_passenger = IntegerProperty(required=False, default=4)

    start = JSONProperty()
    finished = JSONProperty()

    passengers = AsyncRelationshipFrom("User", 'RIDE_TO', model=Ride, cardinality=AsyncZeroOrOne)
    driver = AsyncRelationshipFrom("User", 'DRIVER_TO', model=Travel, cardinality=AsyncOne)
    car = AsyncRelationshipFrom('Automobile', 'DRIVE')

    @property
    async def designated_driver(self):
        return await self.driver.single()

    @property
    async def transport(self):
        return await self.car.single()

    @property
    async def users(self):
        return await self.passengers.all()

    @property
    async def path_routes(self) -> Tuple[LocationData, LocationData]:
        start, finished = self.start, self.finished

        return LocationData(**start), LocationData(**finished)

    @property
    def is_valid(self):
        return not all((
            self.terminate, self.active, self.cancel
        ))

    @property
    async def current_passengers(self):
        return len(await self.passengers.all())


class Rating(AsyncStructuredNode):
    overall = IntegerProperty(required=True, choices=range(1,6))
    punctuality = IntegerProperty(required=True, choices=range(1,6))
    driving_behavior = IntegerProperty(required=True, choices=range(1,6))

    passenger = AsyncRelationshipFrom("User", "RATED")
    schedule = AsyncRelationshipFrom("Schedule", "RATING")

from typing import Required
from neomodel import AsyncStructuredNode, UniqueIdProperty, StringProperty, DateProperty, EmailProperty, \
    BooleanProperty, IntegerProperty, DateTimeProperty, AsyncStructuredRel, \
    AsyncRelationshipTo, AsyncRelationshipFrom, AsyncOne


class RecordTrackingMixin:
    location = StringProperty(required=True)
    latitude = StringProperty(required=True)
    longitude = StringProperty(required=True)


class Ride(AsyncStructuredRel, RecordTrackingMixin):
    time = DateTimeProperty(default_now=True)
    validate = BooleanProperty(default=False)
    cancel = BooleanProperty(default=False)


class Travel(AsyncStructuredRel):
    time = DateTimeProperty(default_now=True)


class User(AsyncStructuredNode):
    ROLES = {
        'S': 'student',
        'D': 'driver',
        'N': 'intern',
        'F': 'staff',
        'A': 'admin'
    }

    code = IntegerProperty(indexed=True, unique_index=True)

    firstname = StringProperty(required=True)
    maternal_surname = StringProperty(required=True)
    paternal_surname = StringProperty(required=True)
    curp = StringProperty(required=True)

    birth_date = DateProperty(required=True)

    email = EmailProperty(required=True, unique_index=True)
    password = StringProperty(required=True)

    valid_user = BooleanProperty(required=False, default=False)

    role = StringProperty(choices=ROLES, default='S')

    cars = AsyncRelationshipTo('Automobile', 'OWNS')
    rides = AsyncRelationshipTo("Schedule", 'RIDE', model=Ride)
    schedules = AsyncRelationshipTo("Schedule", 'TRAVEL', model=Travel)

    @property
    def is_admin(self):
        return False

    @property
    def is_staff(self):
        return False

    @property
    def is_driver(self):
        return self.role == 'D'

    @property
    def is_validate(self):
        return self.valid_user


class Automobile(AsyncStructuredNode):
    code = IntegerProperty(indexed=True, unique_index=True)
    brand = StringProperty(required=True, unique_index=True)
    year = IntegerProperty(required=True)
    model = StringProperty(required=True)

    schedule = AsyncRelationshipTo('Schedule', 'DRIVE')

    car = AsyncRelationshipFrom('User', 'OWNS')


class Record(AsyncStructuredNode, RecordTrackingMixin):
    time = DateTimeProperty(default_now=True)

    origin = AsyncRelationshipFrom('Schedule', 'START', cardinality=AsyncOne)
    tracking = AsyncRelationshipTo('Schedule', 'TRACKING')
    destination = AsyncRelationshipFrom('Schedule', 'END', cardinality=AsyncOne)


class Schedule(AsyncStructuredNode):
    uuid = UniqueIdProperty(indexed=True)

    active = BooleanProperty(required=False, default=False)
    terminate = BooleanProperty(required=False, default=False)
    cancel = BooleanProperty(required=False, default=False)

    price = IntegerProperty(required=True)
    max_passenger = IntegerProperty(required=False, default=4)

    origin = AsyncRelationshipFrom('Record', 'START', cardinality=AsyncOne)
    tracking = AsyncRelationshipTo('Record', 'TRACKING')
    destination = AsyncRelationshipFrom('Record', 'END', cardinality=AsyncOne)

    passengers = AsyncRelationshipFrom("User", 'RIDE', model=Ride)
    driver = AsyncRelationshipFrom("User", 'TRAVEL', model=Travel)
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
    async def path_routes(self):
        return await self.origin.single(), await self.destination.single()

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

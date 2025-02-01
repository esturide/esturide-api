from neomodel import AsyncStructuredNode, UniqueIdProperty, StringProperty, DateProperty, EmailProperty, \
    BooleanProperty, IntegerProperty, DateTimeProperty, AsyncStructuredRel, \
    AsyncRelationshipTo, AsyncRelationshipFrom, AsyncOne, AsyncZeroOrOne

from app.core.enum import RoleUser


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
        'P': 'passenger',
        'D': 'driver',
        'N': 'not-verified',
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

    role = StringProperty(choices=ROLES, default='N')

    cars = AsyncRelationshipTo('Automobile', 'OWNS')
    rides = AsyncRelationshipTo("Schedule", 'RIDE_TO', model=Ride, cardinality=AsyncZeroOrOne)
    schedules = AsyncRelationshipTo("Schedule", 'DRIVER_TO', model=Travel, cardinality=AsyncOne)

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

    @property
    def role_value(self):
        try:
            return RoleUser[User.ROLES[self.role]]
        except KeyError:
            return RoleUser.not_verified


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

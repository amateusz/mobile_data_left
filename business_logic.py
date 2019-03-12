class ServiceDetails:
    # data type.
    DATE, GB, NUMBER, ALIAS = 1, 2, 3, 4  # static ??

    def __init__(self):
        self.NUMBER = None
        self.GB = None
        self.DATE = None
        self.ALIAS = None

    def dict(self):
        if self.GB and self.DATE:
            return dict([__class__.DATE, self.DATE],
                        [__class__.GB, self.GB],
                        [__class__.NUMBER, self.NUMBER],
                        [__class__.ALIAS, self.ALIAS])
        else:
            raise LookupError

    def set(self, key, value):
        self.key = value


class Service:
    # represents more of a account. It assumes, that there can be multiple actual account bound to this account
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.operator = None
        self.country = 'pl'
        self.serviceDetails = ServiceDetails()

    def fetch(self):
        from random import randint
        number = randint(500_000_000, 899_999_999)
        GB = randint(0, 100_0) / 10
        date = randint(0, 365)

        self.serviceDetails.set(ServiceDetails.GB, GB)
        self.serviceDetails.set(ServiceDetails.DATE, date)
        self.serviceDetails.set(ServiceDetails.NUMBER, number)

    def details(self):
        return self.serviceDetails.dict()

    @staticmethod
    def guess_service(username, password):
        guessing = Service(username, password)
        guessing.fetch()
        return guessing.details()

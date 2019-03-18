from my_orange_client import MyOrangeClient
from plus_online_client import PlusOnlineClient


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
    # represents more of a user account. It assumes, that there can be multiple services bound to this account
    # static:
    operators = [MyOrangeClient, PlusOnlineClient]  # this class can be one of those

    def __init__(self, username, password, operator_client):
        # declare properties
        # self.username = username
        # self.password = password
        self.operator_client = operator_client
        self.country = 'pl'
        self.serviceDetails = ServiceDetails()
        # actual init
        print(type(username))
        print(type(password))
        self.token = self.operator_client.giveMeToken(username, password)
        # self.token = 'ffdsfdsamewlkrnlkn435'
        print(self.token)

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
        for operator in __class__.operators:
            try:
                guessed = Service(username, password, operator)
                guessed.fetch()
            except Exception as e:
                raise (e)
            else:
                return guessed
        raise LookupError

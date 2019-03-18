from my_orange_client import MyOrangeClient
from plus_online_client import PlusOnlineClient


class AccountSub(dict):
    # data type.
    DATE = 'dateDue'
    GB = 'GBdue'
    NUMBER = 'msdin'
    ALIAS = 'alias'
    OPERATOR = 'operator'  # statics

    def __init__(self):
        self[__class__.NUMBER] = None
        self[__class__.GB] = None
        self[__class__.DATE] = None
        self[__class__.ALIAS] = None
        self[__class__.OPERATOR] = None

    def __dict__(self):
        if self.GB and self.DATE:
            return dict([__class__.DATE, self.DATE],
                        [__class__.GB, self.GB],
                        [__class__.OPERATOR, self.OPERATOR],
                        # it is redundant. this object will always be bound to the account (upper-levcel entity)
                        [__class__.NUMBER, self.NUMBER],
                        [__class__.ALIAS, self.ALIAS])

        else:
            raise LookupError

    def set(self, key, value):
        self[key] = value


class Account:
    # represents more of a user account. It assumes, that there can be multiple services bound to this account
    # static:
    operators = [MyOrangeClient, PlusOnlineClient]  # this class can be one of those

    def __init__(self, username, password, operator_client):
        # declare properties
        # self.username = username
        # self.password = password
        self.client = operator_client()
        self.country = 'pl'
        self.subAccounts = []
        # actual init
        self.token = self.client.giveMeToken(username, password)

    def fetch_mock(self):
        from random import randint
        number = randint(500_000_000, 899_999_999)
        GB = randint(0, 100_0) / 10
        date = randint(0, 365)

    def fetch(self):
        self.client.authenticate(self.token)
        self.client.refreshDetails(self.token)

        new_subAccount = AccountSub()
        new_subAccount.set(AccountSub.GB, self.client.getGBamount())
        new_subAccount.set(AccountSub.DATE, self.client.getDueToDays())
        new_subAccount.set(AccountSub.NUMBER, self.client.number)
        try:
            new_subAccount.set(AccountSub.OPERATOR, {'text': self.client.friendly_name, 'color': self.client.friendly_color})
        except KeyError:
            new_subAccount.set(AccountSub.OPERATOR, {'text': self.client.friendly_name})
        self.subAccounts.append(new_subAccount)

    def details(self):
        return [subAccount.dict() for subAccount in self.subAccounts]

    @staticmethod
    def guess_operator(username, password, *args):
        for operator in __class__.operators:
            try:
                guessed = Account(username, password, operator)
            except PermissionError as e:
                pass  # handled at higher level
            except Exception as e:
                raise (e)
            else:
                return guessed
        raise LookupError

    @staticmethod
    def serialize(obj):
        # https://stackoverflow.com/questions/18478287/making-object-json-serializable-with-regular-encoder/18561055
        from pickle import dumps
        return dumps(obj).decode('latin1')

    @staticmethod
    def deserialize(str):
        from pickle import loads
        return loads(str.encode('latin1'))

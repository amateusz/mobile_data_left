import unittest


class TestServiceProviders(unittest.TestCase):
    providers_under_test = ['my_orange_client', 'plus_online_client']
    service_providers = {}

    # @unittest.skip
    # def setUp(self):
    #     self.service_providers = {}

    def test_1_import(self):
        for x in __class__.providers_under_test:
            try:
                __class__.service_providers[x] = __import__(x)
                # print("Successfully imported ", x)
            except ImportError as e:
                raise (e)
        self.assertEqual(len(__class__.providers_under_test), len(__class__.service_providers))

    def test_2_authorize_falsch(self):
        for provider in __class__.providers_under_test:
            with self.subTest(provider=provider):
                module = __import__(provider)
                if provider == 'my_orange_client':
                    object = module.MyOrangeClient()
                elif provider == 'plus_online_client':
                    object = module.PlusOnlineClient()
                with self.assertRaises(PermissionError):
                    object.giveMeToken('wrong', 'login')

    def test_3_get_new_token(self):
        for provider in __class__.providers_under_test:
            with self.subTest(provider=provider):
                module = __import__(provider)
                from getpass import getpass
                if provider == 'my_orange_client':
                    object = module.MyOrangeClient()
                    username, password = input('orange: '), getpass()
                elif provider == 'plus_online_client':
                    object = module.PlusOnlineClient()
                    username, password = input('plus: '), getpass()
                self.assertIsNotNone(object.giveMeToken(username, password))



if __name__ == '__main__':
    unittest.main()

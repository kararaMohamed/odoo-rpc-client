from . import BaseTestCase
from openerp_proxy.core import Client
from openerp_proxy.exceptions import LoginException


class TestConnection(BaseTestCase):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.client = Client(self.env.host, protocol=self.env.protocol, port=self.env.port)

    def test_00_connection_simple(self):
        client = self.client
        self.assertIsNone(client.username)
        self.assertIsNone(client.dbname)

        # access to uid with out credentials provided, should cause error
        with self.assertRaises(LoginException):
            client.uid

        # access to uid with out credentials provided, should cause error
        with self.assertRaises(LoginException):
            client.user

    def test_10_create_db(self):
        client = self.client
        if self.env.dbname in client.services.db.list_db():
            return self.skipTest("Database already created")
        cl = client.services.db.create_db(self.env.super_password, self.env.dbname, demo=True, admin_password=self.env.password)

        # cl is object of same class as client, but with credential filled
        self.assertIsInstance(cl, Client)

        # test that uid and user properties are accessible
        self.assertIsNotNone(cl.uid)
        self.assertIsNotNone(cl.user)

    def test_20_connect(self):
        client = self.client
        cl = client.connect(dbname=self.env.dbname, user=self.env.user, pwd=self.env.password)

        # cl is object of same class as client, but with credential filled
        self.assertIsInstance(cl, Client)

        # test that uid and user properties are accessible
        self.assertIsNotNone(cl.uid)
        self.assertIsNotNone(cl.user)

    def test_30_login(self):
        client = self.client
        cl = client.login(self.env.dbname, self.env.user, self.env.password)

        # cl is object of same class as client, but with credential filled
        self.assertIsInstance(cl, Client)

        # test that uid and user properties are accessible
        self.assertIsNotNone(cl.uid)
        self.assertIsNotNone(cl.user)

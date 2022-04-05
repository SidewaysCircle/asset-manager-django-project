from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Laptop, Location
from ..models import Client as testingclient
from ..views.laptopCheckout import laptopCheckoutView

class listTests(TestCase):

    def setUp(self):
        """ Setup test user not super user """
        self.client = Client()
        self.user_raw_password = "password"
        self.user = User.objects.create_user(username='test-std-user',
                                             password=self.user_raw_password)
        self.client.login(username=self.user.username, password=self.user_raw_password)

        self.testSiteDef = Location.objects.create( locName = "test-site-default",
                                                    locAddressOne = "Address Line 1",
                                                    locAddressTwo = "Address Line 2",
                                                    locCity = "testville",
                                                    locPostcode = "UT3 5TO")

        self.testUser = testingclient.objects.create(clientForename = "john",
                                                    clientSurname = "doe",
                                                    clientLoginID = "doej1",
                                                    clientEmail = "john.doe@test.com",
                                                    clientLocation = self.testSiteDef)

        self.list_path = reverse('laptopList')

    def test_get_list_view(self):
        response = self.client.get(self.list_path)
        self.assertEqual(response.status_code, 200)

    def test_empty_asset_list(self):
        response = self.client.get(self.list_path)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['laptopList'], [])

    def test_populated_asset_list(self):
        asset = Laptop.objects.create( laptopBrand = "LENOVO",
                                                laptopModel = "L14",
                                                laptopSerial = "T3STS3R14L",
                                                laptopMemory = 16,
                                                laptopLocation = self.testSiteDef,
                                                laptopUser = self.testUser)
        response = self.client.get(self.list_path)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['laptopList'], [asset])
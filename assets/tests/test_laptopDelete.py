from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Laptop, Location
from ..models import Client as testingclient
from ..views.laptopCheckout import laptopCheckoutView


class RegisterTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_raw_password = "password"
        self.user = User.objects.create_user(username='test-std-user',
                                             password=self.user_raw_password)
        self.superuser = User.objects.create_superuser(username='test-admin-user',
                                                       password=self.user_raw_password)
        #Though only a laptop is being deleted, all models need creating due to foreign key dependancies
        self.testSiteDef = Location.objects.create( locName = "test-site-default",
                                                    locAddressOne = "Address Line 1",
                                                    locAddressTwo = "Address Line 2",
                                                    locCity = "testville",
                                                    locPostcode = "UT3 5TO")

        self.testUser = testingclient.objects.create(   clientForename = "john",
                                                        clientSurname = "doe",
                                                        clientLoginID = "doej1",
                                                        clientEmail = "john.doe@test.com",
                                                        clientLocation = self.testSiteDef)

        self.testasset = Laptop.objects.create( laptopBrand = "LENOVO",
                                                laptopModel = "L14",
                                                laptopSerial = "T3STS3R14L",
                                                laptopMemory = 16,
                                                laptopLocation = self.testSiteDef,
                                                laptopUser = self.testUser)

        self.delete_path = reverse('laptopDelete', kwargs={"pk": self.testasset.id})

    def test_get_happy_path_delete_admin(self):
        #Ensure register page opens
        self.client.login(username=self.superuser.username, password=self.user_raw_password)
        response = self.client.get(self.delete_path)
        self.assertEqual(response.status_code, 200)

    def test_get_sad_path_delete_std(self):
        #Ensure register page opens
        self.client.login(username=self.user.username, password=self.user_raw_password)
        response = self.client.get(self.delete_path)
        self.assertEqual(response.status_code, 403)

    def test_delete_laptop(self):
        self.client.login(username=self.superuser.username, password=self.user_raw_password)
        asset = Laptop.objects.all()
        self.assertEqual(len(asset), 1)
        response = self.client.post(self.delete_path)
        self.assertEqual(response.status_code, 302)
        asset = Laptop.objects.all()
        self.assertEqual(len(asset), 0)


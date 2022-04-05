from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Laptop, Location
from ..models import Client as testingclient
from ..views.laptopCheckout import laptopCheckoutView


class CheckoutTests(TestCase):

    def setUp(self):
        #Only user necessary for these tests is the standard user
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

        self.testasset = Laptop.objects.create( laptopBrand = "LENOVO",
                                                laptopModel = "L14",
                                                laptopSerial = "T3STS3R14L",
                                                laptopMemory = 16,
                                                laptopLocation = self.testSiteDef,
                                                laptopUser = None)
                                                
        self.checkout_path = reverse('laptopCheckout', kwargs={"pk": self.testasset.id})

    def test_get_happy_path_checkout(self):
        #Ensure Checkin Page works
        response = self.client.get(self.checkout_path)
        self.assertEqual(response.status_code, 200)

    def test_laptop_checkout(self):
        #Find test asset
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R14L")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, None)
        #Assign new site & remove user relationship
        data = {
            'laptopUser': self.testUser.id
        }
        response = self.client.post(self.checkout_path, data=data)
        self.assertEqual(response.status_code, 302)
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R14L")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)

    def test_laptop_checkout_no_user(self):
        #Find test asset
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R14L")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, None)
        #Assign new site & remove user relationship
        data = {
            'laptopUser': ""
        }
        response = self.client.post(self.checkout_path, data=data)
        self.assertContains(response, "This field is required.", status_code=400)       

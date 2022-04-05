from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Laptop, Location
from ..models import Client as testingclient
from ..views.laptopCheckin import laptopCheckinView


class CheckinTests(TestCase):

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

        self.testSiteNew = Location.objects.create( locName = "test-site-new",
                                                    locAddressOne = "New Address Line 1",
                                                    locAddressTwo = "New Address Line 2",
                                                    locCity = "New testcity",
                                                    locPostcode = "N3W T5T")

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
                                                
        self.checkin_path = reverse("laptopCheckin", kwargs={"pk": self.testasset.id})

    def test_get_happy_path_checkin(self):
        #Ensure Checkin Page works
        response = self.client.get(self.checkin_path)
        self.assertEqual(response.status_code, 200)

    def test_laptop_checkin(self):
        #Find test asset
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R14L")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)
        #Assign new site & remove user relationship
        data = {
            'laptopLocation': self.testSiteNew.id,
            'laptopUser': ""
        }
        response = self.client.post(self.checkin_path, data=data)
        self.assertEqual(response.status_code, 302)
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R14L")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteNew)
        self.assertIsNone(created_asset.laptopUser)

    def test_laptop_checkin_no_location(self):
        #Find test asset
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R14L")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)
        #Assign new site & remove user relationship
        data = {
            'laptopLocation': "",
            'laptopUser': ""
        }
        response = self.client.post(self.checkin_path, data=data)
        self.assertContains(response, "This field is required.", status_code=400)               
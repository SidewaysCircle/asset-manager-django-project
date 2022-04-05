from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Laptop, Location
from ..models import Client as testingclient
from ..views.laptopCheckout import laptopCheckoutView

class CreateTests(TestCase):

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
                                                
        self.create_path = reverse('laptopCreate')

    def test_get_happy_path_create(self):
        #Ensure register page opens
        response = self.client.get(self.create_path)
        self.assertEqual(response.status_code, 200)

    def test_create_laptop_success(self):
        data = {
            'laptopBrand': "LENOVO",
            'laptopModel': "L14",
            'laptopSerial': "T3STS3R",
            'laptopMemory': 16,
            'laptopLocation': self.testSiteDef.id,
            'laptopUser': ""
        }
        response = self.client.post(self.create_path, data=data)
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, None)

        view_path = reverse('laptopList')
        
        self.assertRedirects(response, view_path, status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_create_laptop_no_brand(self):
        data = {
            'laptopBrand': "",
            'laptopModel': "L14",
            'laptopSerial': "T3STS3R",
            'laptopMemory': 16,
            'laptopLocation': self.testSiteDef.id,
            'laptopUser': ""
        }
        response = self.client.post(self.create_path, data=data)
        self.assertContains(response, "This field is required.", status_code=400)        

    def test_create_laptop_no_model(self):
        data = {
            'laptopBrand': "LENOVO",
            'laptopModel': "",
            'laptopSerial': "T3STS3R",
            'laptopMemory': 16,
            'laptopLocation': self.testSiteDef.id,
            'laptopUser': ""
        }
        response = self.client.post(self.create_path, data=data)
        self.assertContains(response, "This field is required.", status_code=400)     

    def test_create_laptop_no_serial(self):
        data = {
            'laptopBrand': "LENOVO",
            'laptopModel': "L14",
            'laptopSerial': "",
            'laptopMemory': 16,
            'laptopLocation': self.testSiteDef.id,
            'laptopUser': ""
        }
        response = self.client.post(self.create_path, data=data)
        self.assertContains(response, "This field is required.", status_code=400)       

    def test_create_laptop_no_memory(self):
        data = {
            'laptopBrand': "LENOVO",
            'laptopModel': "L14",
            'laptopSerial': "T3STS3R",
            'laptopMemory': "",
            'laptopLocation': self.testSiteDef.id,
            'laptopUser': ""
        }
        response = self.client.post(self.create_path, data=data)
        self.assertContains(response, "This field is required.", status_code=400)      

    def test_create_laptop_no_location(self):
        data = {
            'laptopBrand': "LENOVO",
            'laptopModel': "L14",
            'laptopSerial': "T3STS3R",
            'laptopMemory': 16,
            'laptopLocation': "",
            'laptopUser': ""
        }
        response = self.client.post(self.create_path, data=data)
        self.assertContains(response, "This field is required.", status_code=400)      

    def test_create_laptop_invalid_brand(self):
        data = {
            'laptopBrand': "invalid brand",
            'laptopModel': "L14",
            'laptopSerial': "T3STS3R",
            'laptopMemory': 16,
            'laptopLocation': self.testSiteDef.id,
            'laptopUser': ""
        }
        response = self.client.post(self.create_path, data=data)
        self.assertContains(response, "Laptop brand is not used by the business", status_code=400)      

    def test_create_laptop_invalid_memory(self):
        data = {
            'laptopBrand': "invalid brand",
            'laptopModel': "L14",
            'laptopSerial': "T3STS3R",
            'laptopMemory': 13,
            'laptopLocation': self.testSiteDef.id,
            'laptopUser': ""
        }
        response = self.client.post(self.create_path, data=data)
        self.assertContains(response, "The RAM capacity is incorrect. Please enter a valid value", status_code=400)   


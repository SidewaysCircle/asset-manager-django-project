from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Laptop, Location
from ..models import Client as testingclient
from ..views.laptopCheckin import laptopCheckinView


class updateTests(TestCase):
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

        self.testUser = testingclient.objects.create(clientForename = "john",
                                                    clientSurname = "doe",
                                                    clientLoginID = "doej1",
                                                    clientEmail = "john.doe@test.com",
                                                    clientLocation = self.testSiteDef)

        self.testasset = Laptop.objects.create( laptopBrand = "LENOVO",
                                                laptopModel = "L14",
                                                laptopSerial = "T3STS3R",
                                                laptopMemory = 16,
                                                laptopLocation = self.testSiteDef,
                                                laptopUser = self.testUser)
                                                
        self.update_path = reverse('laptopUpdate', kwargs={"pk": self.testasset.id})

    def test_get_happy_path_update(self):
        #Ensure Checkin Page works
        response = self.client.get(self.update_path)
        self.assertEqual(response.status_code, 200)

    def test_laptop_update_Brand(self):
        #Find test asset
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)
        #Assign new site & remove user relationship
        data = {
            'laptopBrand': "HP",
            'laptopModel': "L14",
            'laptopSerial': "T3STS3R",
            'laptopMemory': 16,
            'laptopLocation': self.testSiteDef.id,
            #'laptopUser' will remain blank as property is changed in Checkin/Checkout
            'laptopUser': self.testUser.id
        }
        response = self.client.post(self.update_path, data=data)
        self.assertEqual(response.status_code, 302)
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "HP")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)

    def test_laptop_update_Model(self):
        #Find test asset
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)
        #Assign new site & remove user relationship
        data = {
            'laptopBrand': "LENOVO",
            'laptopModel': "Elitebook G4",
            'laptopSerial': "T3STS3R",
            'laptopMemory': 16,
            'laptopLocation': self.testSiteDef.id,
            #'laptopUser' will remain blank as property is changed in Checkin/Checkout
            'laptopUser': self.testUser.id
        }
        response = self.client.post(self.update_path, data=data)
        self.assertEqual(response.status_code, 302)
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "Elitebook G4")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)

    def test_laptop_update_Serial(self):
        #Find test asset
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)
        #Assign new site & remove user relationship
        data = {
            'laptopBrand': "LENOVO",
            'laptopModel': "L14",
            'laptopSerial': "N3WS3R14L",
            'laptopMemory': 16,
            'laptopLocation': self.testSiteDef.id,
            #'laptopUser' will remain blank as property is changed in Checkin/Checkout
            'laptopUser': self.testUser.id
        }
        response = self.client.post(self.update_path, data=data)
        self.assertEqual(response.status_code, 302)
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "N3WS3R14L")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)

    def test_laptop_update_Memory(self):
        #Find test asset
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)
        #Assign new site & remove user relationship
        data = {
            'laptopBrand': "LENOVO",
            'laptopModel': "L14",
            'laptopSerial': "T3STS3R",
            'laptopMemory': 8,
            'laptopLocation': self.testSiteDef.id,
            #'laptopUser' will remain blank as property is changed in Checkin/Checkout
            'laptopUser': self.testUser.id
        }
        response = self.client.post(self.update_path, data=data)
        self.assertEqual(response.status_code, 302)
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 8)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)

    def test_laptop_update_Location(self):
        #Find test asset
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)
        #Assign new site & remove user relationship
        data = {
            'laptopBrand': "LENOVO",
            'laptopModel': "L14",
            'laptopSerial': "T3STS3R",
            'laptopMemory': 16,
            'laptopLocation': self.testSiteNew.id,
            'laptopUser': self.testUser.id
        }
        response = self.client.post(self.update_path, data=data)
        self.assertEqual(response.status_code, 302)
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteNew)
        self.assertEqual(created_asset.laptopUser, self.testUser)

    def test_laptop_update_no_brand(self):
        #Find test asset
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)
        #Assign new site & remove user relationship
        data = {
            'laptopBrand': "",
            'laptopModel': "L14",
            'laptopSerial': "T3STS3R",
            'laptopMemory': 16,
            'laptopLocation': self.testSiteDef.id,
            'laptopUser': self.testUser
        }
        response = self.client.post(self.update_path, data=data)
        self.assertContains(response, "This field is required.", status_code=400)  

    def test_laptop_update_no_model(self):
        #Find test asset
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)
        #Assign new site & remove user relationship
        data = {
            'laptopBrand': "LENOVO",
            'laptopModel': "",
            'laptopSerial': "T3STS3R",
            'laptopMemory': 16,
            'laptopLocation': self.testSiteDef.id,
            'laptopUser': self.testUser
        }
        response = self.client.post(self.update_path, data=data)
        self.assertContains(response, "This field is required.", status_code=400)  

    def test_laptop_update_no_serial(self):
        #Find test asset
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)
        #Assign new site & remove user relationship
        data = {
            'laptopBrand': "LENOVO",
            'laptopModel': "L14",
            'laptopSerial': "",
            'laptopMemory': 16,
            'laptopLocation': self.testSiteDef.id,
            'laptopUser': self.testUser
        }
        response = self.client.post(self.update_path, data=data)
        self.assertContains(response, "This field is required.", status_code=400)  

    def test_laptop_update_no_memory(self):
        #Find test asset
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)
        #Assign new site & remove user relationship
        data = {
            'laptopBrand': "LENOVO",
            'laptopModel': "L14",
            'laptopSerial': "T3STS3R",
            'laptopMemory': "",
            'laptopLocation': self.testSiteDef.id,
            'laptopUser': self.testUser
        }
        response = self.client.post(self.update_path, data=data)
        self.assertContains(response, "This field is required.", status_code=400)  

    def test_laptop_update_no_location(self):
        #Find test asset
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)
        #Assign new site & remove user relationship
        data = {
            'laptopBrand': "LENOVO",
            'laptopModel': "L14",
            'laptopSerial': "T3STS3R",
            'laptopMemory': 16,
            'laptopLocation': "",
            'laptopUser': self.testUser
        }
        response = self.client.post(self.update_path, data=data)
        self.assertContains(response, "This field is required.", status_code=400)  

    def test_laptop_update_invalid_model(self):
        #Find test asset
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)
        #Assign new site & remove user relationship
        data = {
            'laptopBrand': "invalid brand",
            'laptopModel': "L14",
            'laptopSerial': "T3STS3R",
            'laptopMemory': 16,
            'laptopLocation': self.testSiteDef.id,
            'laptopUser': self.testUser
        }
        response = self.client.post(self.update_path, data=data)
        self.assertContains(response, "Laptop brand is not used by the business", status_code=400)  

    def test_laptop_update_invalid_memory(self):
        #Find test asset
        assets = Laptop.objects.all()
        self.assertEqual(len(assets), 1)
        created_asset = assets[0]
        self.assertEqual(created_asset.laptopBrand, "LENOVO")
        self.assertEqual(created_asset.laptopModel, "L14")
        self.assertEqual(created_asset.laptopSerial, "T3STS3R")
        self.assertEqual(created_asset.laptopMemory, 16)
        self.assertEqual(created_asset.laptopLocation, self.testSiteDef)
        self.assertEqual(created_asset.laptopUser, self.testUser)
        #Assign new site & remove user relationship
        data = {
            'laptopBrand': "LENOVO",
            'laptopModel': "L14",
            'laptopSerial': "T3STS3R",
            'laptopMemory': 13,
            'laptopLocation': self.testSiteDef.id,
            'laptopUser': self.testUser
        }
        response = self.client.post(self.update_path, data=data)
        self.assertContains(response, "The RAM capacity is incorrect. Please enter a valid value", status_code=400)  







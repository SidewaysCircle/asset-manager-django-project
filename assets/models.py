#from typing_extensions import Required
from django.db import models
from django.urls import reverse

# Create your models here.

class Location(models.Model):
    locName = models.CharField(max_length=125)
    locAddressOne = models.CharField(max_length=125)
    locAddressTwo = models.CharField(max_length=125)
    locCity = models.CharField(max_length=35)
    locPostcode = models.CharField(max_length=8)

    def __str__(self):
        ret = self.locName
        return ret

class Client(models.Model):
    clientForename = models.CharField(max_length=45)
    clientSurname = models.CharField(max_length=45)
    clientLoginID = models.CharField(max_length=10)
    clientEmail = models.CharField(max_length=145)
    clientLocation = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        ret = self.clientForename + ' ' + self.clientSurname + ' | ' + self.clientLoginID
        return ret

class Laptop(models.Model):

    laptopBrand = models.CharField(max_length=15)#
    laptopModel = models.CharField(max_length=25)
    laptopSerial = models.CharField(max_length=10)
    laptopMemory = models.IntegerField()
    laptopLocation = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    laptopUser = models.ForeignKey(Client, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        ret = self.laptopBrand + ',' + self.laptopModel + ',' + self.laptopSerial
        return ret

    def get_absolute_url(self):
        return reverse("laptopList")
    
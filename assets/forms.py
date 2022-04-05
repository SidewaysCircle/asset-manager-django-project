from django import forms
from .models import Laptop, Location
from django.core.exceptions import ValidationError


class createLaptopForm(forms.ModelForm):

    class Meta:
        model = Laptop
        fields = [
            'laptopBrand',
            'laptopModel',
            'laptopSerial',
            'laptopMemory',
            'laptopLocation',
            'laptopUser'
        ]

    def clean_laptopBrand(self):
        validBrands = ["DELL", "HP", "LENOVO", "APPLE", "MICROSOFT"]
        laptopBrand = self.cleaned_data['laptopBrand'].upper()
        if self.fieldIsNoneOrEmpty(laptopBrand):
            raise ValidationError("Laptop Brand is required")
        if laptopBrand not in validBrands:
            raise ValidationError("Laptop brand is not used by the business")
        return laptopBrand

    def clean_laptopModel(self):
        laptopModel = self.cleaned_data['laptopModel']
        if self.fieldIsNoneOrEmpty(laptopModel):
            raise ValidationError("Laptop Model is required")
        if len(laptopModel) > 25:
            raise ValidationError("Laptop Model needs to be less than 25 characters")
        if not self.fieldIsAlphanumeric(laptopModel.replace(" ", "")):
            raise ValidationError("The laptop model will only contain A-z and 0-9 and white space")
        return laptopModel
    
    def clean_laptopSerial(self):
        laptopSerial = self.cleaned_data['laptopSerial']
        if self.fieldIsNoneOrEmpty(laptopSerial):
            raise ValidationError("Serial Number is required")
        if len(laptopSerial) > 10:
            raise ValidationError("Laptop Model needs to be less than 10 characters")
        if not self.fieldIsAlphanumeric(laptopSerial):
            raise ValidationError("The serial number will only contain A-z and 0-9")
        return laptopSerial

    def clean_laptopMemory(self):
        validMemory = [4, 8, 16, 32, 64, 128]
        laptopMemory = self.cleaned_data['laptopMemory']
        if laptopMemory not in validMemory:
            raise ValidationError("The RAM capacity is incorrect. Please enter a valid value")
        return laptopMemory

    @staticmethod
    def fieldIsNumeric(field) -> bool:
        #Verify that field is numeric
        return field.isnumeric()


    @staticmethod
    def fieldIsAlphanumeric(field) -> bool:
        #Verify that field is alphanumeric
        return field.isalnum()

    @staticmethod
    def fieldIsNoneOrEmpty(field) -> bool:
        #Verify that field not empty
        return field is None or field == ''

class checkoutLaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = [
            'laptopUser'
        ]

    def __init__(self, *args, **kwargs):
        super(checkoutLaptopForm, self).__init__(*args, **kwargs)
        self.fields['laptopUser'].required=True

class checkinLaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = [
            'laptopLocation',
            'laptopUser'
        ]

    def __init__(self, *args, **kwargs):
        super(checkinLaptopForm, self).__init__(*args, **kwargs)
        self.fields['laptopUser'].required=False

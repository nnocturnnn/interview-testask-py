from django import forms
from django.contrib.auth.models import User
from adress_book.models import ContactInfo, MobileNumber


class UserRegistration(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)


class ContactAdd(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ('full_name', 'nick_name', 'address', 'date_of_birth',)


class MobileNumberSave(forms.ModelForm):
    class Meta:
        model = MobileNumber
        fields = ('phone_number',)

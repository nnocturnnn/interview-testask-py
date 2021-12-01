from django.db import models

from django.contrib.auth.models import User


# Create your models here.

class ContactInfo(models.Model):
    """  To save the contact information """

    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    full_name = models.CharField(max_length=50)
    nick_name = models.CharField(max_length=50)
    address = models.CharField(max_length=264)
    date_of_birth = models.CharField(max_length=20)

    def __str__(self):
        return self.user_name.username


class MobileNumber(models.Model):
    """  To save multiple contact number for any person """

    phone_id = models.ForeignKey(ContactInfo, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.phone_id.user_name.username

from django.db import models
from Administrator.models import *


# Create your models here.
class tbl_user(models.Model):
    user_name=models.CharField(max_length=30)
    user_email=models.CharField(max_length=30)
    user_password=models.CharField(max_length=30)
    user_contact=models.CharField(max_length=30)
    user_dob=models.DateField()
    user_photo=models.FileField(upload_to="Assets/UserDocs/")
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)




class tbl_owner(models.Model):
    owner_name = models.CharField(max_length=100)
    owner_email = models.CharField(max_length=100)
    owner_password = models.CharField(max_length=100)
    owner_phone = models.CharField(max_length=15)
    owner_address = models.CharField(max_length=200)
    owner_photo = models.FileField(upload_to="Assets/OwnerDocs/")
    owner_proof = models.FileField(upload_to="Assets/OwnerDocs/")
    place = models.ForeignKey(tbl_place, on_delete=models.CASCADE)
    owner_status = models.IntegerField(default=0)

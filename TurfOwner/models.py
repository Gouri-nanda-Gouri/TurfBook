from django.db import models
from Guest.models import *

# Create your models here.
class tbl_turf(models.Model):
    owner=models.ForeignKey(tbl_owner,on_delete=models.CASCADE)
    turf_name=models.CharField(max_length=100)
    turf_description=models.CharField(max_length=200)
    turf_capacity=models.IntegerField()
    turf_image=models.FileField(upload_to="Assets/Turf/")
    turf_contact_number=models.CharField(max_length=15)
    turf_status=models.IntegerField(default=0)
    truf_doj=models.DateField(auto_now_add=True)
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)

class tbl_turf_gallery(models.Model):
    turf=models.ForeignKey(tbl_turf,on_delete=models.CASCADE)
    gallery_image=models.FileField(upload_to="Assets/TurfGallery/")


class tbl_turf_sports(models.Model):
    turf=models.ForeignKey(tbl_turf,on_delete=models.CASCADE)
    sport=models.ForeignKey(tbl_sports,on_delete=models.CASCADE)


class tbl_slot(models.Model):
    turf=models.ForeignKey(tbl_turf,on_delete=models.CASCADE)
    slot_time=models.CharField(max_length=50)
    slot_amount=models.DecimalField(max_digits=6,decimal_places=2)






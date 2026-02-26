from django.db import models

# Create your models here.
class tbl_district(models.Model):
    district_name=models.CharField(max_length=30)

class tbl_admin(models.Model):
    admin_name=models.CharField(max_length=30)
    admin_email=models.CharField(max_length=30)
    admin_password=models.CharField(max_length=30)

class tbl_category(models.Model):
    category_name=models.CharField(max_length=30)    


class tbl_place(models.Model):
    place_name=models.CharField(max_length=30)  
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)

class tbl_sports(models.Model):
    sports_name=models.CharField(max_length=30)
    required_players = models.IntegerField(default=1)   

    


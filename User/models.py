from django.db import models
from Guest.models import *
from TurfOwner.models import *
from Administrator.models import *

class tbl_booking(models.Model):
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    slot=models.ForeignKey(tbl_slot,on_delete=models.CASCADE)
    sport=models.ForeignKey(tbl_sports,on_delete=models.CASCADE)
    booking_todate=models.DateField()
    booking_date=models.DateField(auto_now_add=True)
    booking_amount=models.DecimalField(max_digits=8,decimal_places=2,null=True)
    # booking_amount is the 30% advance calculated at time of booking, stored for reference. Actual payment can be done later, and may differ if slot amount changes.
    total_amount=models.DecimalField(max_digits=8,decimal_places=2,null=True)
    # total total_amount is calculated at time of booking as players × slot amount, and stored for reference. Actual payment can be done later, and may differ if slot amount changes.
    booking_status=models.IntegerField(default=0)
    booking_players=models.IntegerField(default=1) 


class tbl_request(models.Model):
    booking = models.ForeignKey(tbl_booking, on_delete=models.CASCADE)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    slot = models.ForeignKey(tbl_slot, on_delete=models.CASCADE)
    sport = models.ForeignKey(tbl_sports, on_delete=models.CASCADE)

    request_players = models.IntegerField()
    joined_players = models.IntegerField(default=0)

    request_description = models.CharField(max_length=200)

    request_status = models.IntegerField(default=0)  # 0=open 1=closed
    created_date = models.DateField(auto_now_add=True)

class tbl_request_join(models.Model):
    request = models.ForeignKey(tbl_request, on_delete=models.CASCADE)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    joined_date = models.DateField(auto_now_add=True)

class tbl_refund(models.Model):

    booking = models.ForeignKey(tbl_booking,on_delete=models.CASCADE)
    user = models.ForeignKey(tbl_user,on_delete=models.CASCADE)

    refund_reason = models.CharField(max_length=200)

    refund_status = models.IntegerField(default=0)
    # 0 = pending
    # 1 = approved
    # 2 = rejected

    refund_date = models.DateTimeField(auto_now_add=True)


class tbl_rating(models.Model):
    rating_data=models.IntegerField()
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    user_review=models.CharField(max_length=500)
    truf=models.ForeignKey(tbl_turf,on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now_add=True)


class tbl_complaint(models.Model):
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    complaint_title=models.CharField(max_length=100)
    complaint_content=models.CharField(max_length=500)
    complaint_status=models.IntegerField(default=0) 
    complaint_date=models.DateTimeField(auto_now_add=True)
    complaint_reply=models.CharField(max_length=500,null=True)


class tbl_feedback(models.Model):
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    feedback_content=models.CharField(max_length=500)
    feedback_date=models.DateTimeField(auto_now_add=True)
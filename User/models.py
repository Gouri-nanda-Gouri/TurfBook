from django.db import models
from Guest.models import *
from TurfOwner.models import *

class tbl_booking(models.Model):
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    slot=models.ForeignKey(tbl_slot,on_delete=models.CASCADE)
    booking_todate=models.DateField()
    booking_date=models.DateField(auto_now_add=True)
    booking_amount=models.DecimalField(max_digits=8,decimal_places=2,null=True)
    # booking_amount is the 30% advance calculated at time of booking, stored for reference. Actual payment can be done later, and may differ if slot amount changes.
    total_amount=models.DecimalField(max_digits=8,decimal_places=2,null=True)
    # total total_amount is calculated at time of booking as players × slot amount, and stored for reference. Actual payment can be done later, and may differ if slot amount changes.
    booking_status=models.IntegerField(default=0)
    booking_players=models.IntegerField(default=1) 
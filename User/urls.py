from django.urls import path
from User import views

app_name="User"

urlpatterns = [
     path('HomePage/',views.HomePage, name="HomePage"),
     path('MyProfile/',views.MyProfile, name="MyProfile"),
     path('EditProfile/',views.EditProfile, name="EditProfile"),
     path('ChangePassword/',views.ChangePassword, name="ChangePassword"),


     path('ViewTurf/',views.ViewTurf, name="ViewTurf"),
     path('ViewSlot/<int:tid>',views.ViewSlot,name="ViewSlot"),
     path('Ajaxturf/',views.Ajaxturf, name="Ajaxturf"),  


     # path('BookSlot/<int:sid>/',views.BookSlot, name="BookSlot"),
     path('ConfirmBooking/<int:sid>/',views.ConfirmBooking, name="ConfirmBooking"),
     path('MyBookings/',views.MyBookings,name="MyBookings"),
     path('CancelBooking/<int:bid>',views.CancelBooking,name="CancelBooking"),
    
    path("payment/<int:bid>",views.payment,name="payment"),
    path('loader/',views.loader, name='loader'),
    path('paymentsuc/',views.paymentsuc, name='paymentsuc'),

    path('AddRequest/<int:bid>/',views.AddRequest, name="AddRequest"),
    path('ViewRequest/',views.ViewRequest,name="ViewRequest"),

    path('JoinRequest/<int:rid>', views.JoinRequest, name="JoinRequest"),
]
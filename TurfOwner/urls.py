from django.urls import path
from TurfOwner import views

app_name="TurfOwner"

urlpatterns = [
     path('Sports/',views.Sports, name="Sports"),
     path('MyProfile/',views.MyProfile, name="MyProfile"),

     path('EditProfile/',views.EditProfile, name="EditProfile"),
     path('ChangePassword/',views.ChangePassword, name="ChangePassword"),
     path('HomePage/',views.HomePage, name="HomePage"),
     path('AddTurf/',views.AddTurf, name="AddTurf"),
     path('MyTurf/',views.MyTurf, name="MyTurf"),
     path('DeleteTurf/<int:did>/',views.DeleteTurf, name="DeleteTurf"),
     path('AddGallery/<int:tid>',views.AddGallery,name="AddGallery"),
path('AddTurfSports/<int:tid>',views.AddTurfSports,name="AddTurfSports"),
path('AddSlot/<int:tid>',views.AddSlot,name="AddSlot"),
     path('ViewBookings/',views.ViewBookings,name="ViewBookings"),
path('ApproveBooking/<int:bid>',views.ApproveBooking,name="ApproveBooking"),
path('RejectBooking/<int:bid>',views.RejectBooking,name="RejectBooking"),

    path('logout/',views.logout,name="logout"),


]
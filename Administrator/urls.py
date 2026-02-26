from django.urls import path
from Administrator import views



app_name="Administrator"

urlpatterns = [
     path('District/',views.District, name="District"),
     path('deleteDistrict/<int:did>/',views.DeleteDistrict,name="DeleteDistrict"),
     path('updateDistrict/<int:did>/',views.UpdateDistrict,name="UpdateDistrict"),

     path('AdminRegistration/',views.AdminRegistration),
     
     path('Category/',views.Category,name="Category"),
     path('deleteCategory/<int:cid>/',views.DeleteCategory,name="DeleteCategory"),
     path('UpdateCategory/<int:cid>/',views.UpdateCategory,name="UpdateCategory"),

     path('AdminRegistration/',views.AdminRegistration,name="AdminRegistration"),
     path('deleteAdminRegistration/<int:aid>/',views.DeleteAdminRegistration,name="DeleteAdminRegistration"),
     path('UpdateAdminRegistration/<int:aid>/',views.UpdateAdminRegistration,name="UpdateAdminRegistration"),
     
     path('Place/',views.Place, name="Place"),
     path('deletePlace/<int:pid>/',views.DeletePlace,name="DeletePlace"),
     path('editplace/<int:eid>/',views.editplace,name="editplace"),

     path('HomePage/',views.HomePage, name="HomePage"),

     path('UserList/',views.UserList,name="UserList"),

     path('UserAccept/<int:uid>/',views.UserAccept,name="UserAccept"),
     path('UserReject/<int:uid>/',views.UserReject,name="UserReject"),

     path('OwnerVerification/',views.OwnerVerification,name="OwnerVerification"), 
     path('ApproveOwner/<int:aid>/',views.ApproveOwner,name="ApproveOwner"),
     path('RejectOwner/<int:rid>/',views.RejectOwner,name="RejectOwner"),

     path('TurfVerification/',views.TurfVerification,name="TurfVerification"),
     path('ApproveTurf/<int:aid>/',views.ApproveTurf,name="ApproveTurf"),
     path('RejectTurf/<int:rid>/',views.RejectTurf,name="RejectTurf"),

     path('Sports/',views.Sports,name="Sports"),
     path('deleteSports/<int:sid>/',views.DeleteSports,name="DeleteSports"),
     path('updateSports/<int:uid>/',views.UpdateSports,name="UpdateSports"),

     path('ViewRequests/',views.ViewRequests,name="ViewRequests"),

     path('ViewBookings/',views.ViewBookings,name="ViewBookings"),



]
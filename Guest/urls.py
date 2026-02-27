from django.urls import path
from Guest import views



app_name="Guest"

urlpatterns = [
     path('index/',views.index, name="index"),
     path('UserRegistration/',views.UserRegistration, name="UserRegistration"),
     path('Ajaxplace/',views.Ajaxplace,name="Ajaxplace"),

     path('Login/',views.Login, name="Login"),
      
     path('OwnerRegistration/',views.owner_registration, name="OwnerRegistration"),
     path('Contact/',views.Contact, name="Contact"),

]
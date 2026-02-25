from django.urls import path,include
from Basics import views


urlpatterns = [
    path('sum/',views.Sum),
    path('Calculator/',views.Calculator),
]
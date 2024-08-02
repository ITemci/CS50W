from django.urls import path
from . import views

urlpatterns=[
    path("", views.index,name="index"),
    path("ion",views.ion,name="ion"),
    path("<str:name>", views.greet, name="greet")
]
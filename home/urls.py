from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('add_trip', views.add_trip, name="add_trip"),
]
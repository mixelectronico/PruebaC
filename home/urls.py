from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('add_trip', views.add_trip, name="add_trip"),
]
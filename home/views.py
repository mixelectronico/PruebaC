from django.shortcuts import render, redirect
from django.contrib import messages
from login.models import User
from .models import *


# Create your views here.
def home(request):
    reg_user = request.session['user']
    user_tips_list=Trip.objects.filter(creator=reg_user) | Trip.objects.filter(joined_user=reg_user) 
    other_trips_list= Trip.objects.exclude(creator=reg_user) | Trip.objects.exclude(joined_user=reg_user)
    context = {
        "trips" : user_tips_list,
        "other_plans" : other_trips_list,
    }
    return render(request, 'home/index.html', context)


def add_trip(request):
    user = request.session['user']
    destination = request.POST['destination']
    description = request.POST['description']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    Trip.objects.create(destination=destination, description=description, start_date=start_date, end_date=end_date, creator=user)
    return redirect('travels/')


# TODO: Crear funcionalidad Join Trip
# TODO: Mostrar el detalle de los viajes (localhost:8000/travel/destinations)
# TODO: Terminar la funcion add_trip (Validacion)
# TODO: ESTO ES UN TEST
from django.shortcuts import render, redirect
from django.contrib import messages
from login.models import User
from .models import *


# Create your views here.
def home(request):
    user_tips_list=Trip.objects.filter(creator=request.session['user_id']) | Trip.objects.filter(joined_user=request.session['user_id']) 
    other_trips_list= Trip.objects.exclude(creator=request.session['user_id']).exclude(joined_user=request.session['user_id'])
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
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *


def home(request):
    user_tips_list = Trip.objects.filter(creator=request.session['user_id']) | Trip.objects.filter(joined_user=request.session['user_id'])
    other_trips_list = Trip.objects.exclude(creator=request.session['user_id']).exclude(joined_user=request.session['user_id'])
    context = {
        "trips": user_tips_list,
        "other_plans": other_trips_list,
    }
    return render(request, 'home/index.html', context)


def add_trip(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['user_id'])
        destination = request.POST['destination']
        description = request.POST['description']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        errors = Trip.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, msg in errors.items():
                messages.error(request, msg)
            return redirect('add_trip')

        Trip.objects.create(destination=destination, description=description, start_date=start_date, end_date=end_date,
                            creator=user)
        return redirect('check_user')

    return render(request, 'home/trip_form.html')


# TODO: Crear funcionalidad Join Trip
# TODO: Mostrar el detalle de los viajes (localhost:8000/travel/destinations)
# TODO: ESTO ES UN TEST

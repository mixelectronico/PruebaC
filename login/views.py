from home.models import Trip
from django.shortcuts import render, redirect
from django.contrib import messages
from time import gmtime, strftime
import bcrypt

from .models import User


def login(request):
    return render(request, 'login.html')


def registrar(request):
    return render(request, 'registro.html')


def inicio(request):
    usuario = User.objects.filter(email=request.POST['email'])
    errores = User.objects.validar_login(request.POST, usuario)

    if len(errores) > 0:
        for key, msg in errores.items():
            messages.error(request, msg)
        return redirect('/')
    else:
        request.session['user_id'] = usuario[0].id
        return redirect('home/')


def registro(request):
    #validacion de parametros
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, msg in errors.items():
            messages.error(request, msg)
        return redirect('/registrar')

    else:
        # encriptar password
        password = User.objects.encriptar(request.POST['password'])
        decode_hash_pw = password.decode('utf-8')
        # crear usuario
        if request.POST['rol'] == '1':
            user = User.objects.create(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                email=request.POST['email'],
                password=decode_hash_pw,
                rol=1,
            )
        else:
            user = User.objects.create(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                email=request.POST['email'],
                password=decode_hash_pw,
                rol=2,
            )
        request.session['user_id'] = user.id
    return redirect('home/')


def logout(request):
    request.session.flush()
    return redirect('/')

def add_trip(request):
    user = User.objects.get(id=request.session['user_id'])
    destination = request.POST['destination']
    description = request.POST['description']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    Trip.objects.create(destination=destination, description=description, start_date=start_date, end_date=end_date, creator=user)
    return redirect('travels/')

def list_trips(request):
    reg_user = User.objects.get(id=request.session['user_id'])
    user_tips_list=Trip.objects.filter(creator=reg_user) | Trip.objects.filter(joined_user=reg_user) 
    other_trips_list= Trip.objects.exclude(creator=reg_user) | Trip.objects.exclude(joined_user=reg_user)
    context = {
        "active_user": reg_user,
        "user_trips" : user_tips_list,
        "other_trips" : other_trips_list,
    }
    return render(request, 'home.html', context)
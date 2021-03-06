from django.shortcuts import render, redirect
from django.contrib import messages

from .models import User


def check_user(request):
    if 'user_id' not in request.session:
        return redirect('login')
    return redirect('home')


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
        return redirect('login')
    else:
        request.session['user_id'] = usuario[0].id
        request.session['name'] = usuario[0].nombre
        request.session['last_name'] = usuario[0].apellido
        return redirect('home')


def registro(request):
    # validacion de parametros
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, msg in errors.items():
            messages.error(request, msg)
        return redirect('registrar')

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
    return redirect('home')


def logout(request):
    request.session.flush()
    return redirect('check_user')

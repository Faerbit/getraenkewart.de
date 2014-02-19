from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from getraenkewart.forms import RegistrationForm

REGISTRATION_SUCCESS = "Neuen Benutzer erfolgreich angelegt. Bitte warte auf deine Aktivierung."
LOGIN_SUCCESFUL = "Erfolgreich eingeloggt!"
LOGOUT_SUCCESFUL = "Erfolgreich ausgeloggt!"
WRONG_PASSWORD_ERROR = "Dein Passwort oder dein Benutzername ist falsch."
NOT_ACTIVE_ERROR = "Du bist noch nicht aktiviert! Frag mal nach."

def index(request):
    context = standard_checks(request, "start")
    return render (request, "getraenkewart/index.html", context)

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate (username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            messages.success(request, LOGIN_SUCCESFUL)
            context = standard_checks(request, "start")
            return render (request, "getraenkewart/index.html", context)
        else:
            messages.error(request, NOT_ACTIVE_ERROR) 
            context = standard_checks(request, "start")
            return render (request, "getraenkewart/index.html", context)
    else:
        messages.error(request, WRONG_PASSWORD_ERROR) 
        context = standard_checks(request, "start")
        return render (request, "getraenkewart/index.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, LOGOUT_SUCCESFUL)
    context = standard_checks(request, "start")
    return render(request, "getraenkewart/index.html", context)

def register(request):
    if request.method =="GET":
        form = RegistrationForm()
        context = standard_checks(request, "start")
        context.update({"form":form})
        return render(request, "getraenkewart/register.html", context)
    else:
        form = RegistrationForm(request.POST)
        form.full_clean()
        if form.is_valid():
            first_name  = form.cleaned_data['first_name']
            last_name   = form.cleaned_data['last_name']
            email       = form.cleaned_data["email"]
            username    = form.cleaned_data['username']
            password    = form.cleaned_data['password']
            password2   = form.cleaned_data['password2']
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = False
            user.save()
            messages.success(request, REGISTRATION_SUCCESS)
            return redirect(index)
        else:
            for _, error in form.errors.items():
                messages.error(request, error)
            context = standard_checks(request, "start")
            context.update({"form":form})
            return render(request, "getraenkewart/register.html", context)

def standard_checks(request, active_nav):
    if request.user.is_authenticated():
        name = request.user.first_name
    else:
        name = ""
    if request.user.is_staff:
        return {'name':name, 'is_staff':True, 'active_nav':active_nav}
    else:
        return {'name':name, 'is_staff':False, 'active_nav':active_nav}

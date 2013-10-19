from django.shortcuts import render
#from getraenke.views import generate_bier_chart
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def index(request):
    #context = dict(list({'chart':generate_bier_chart(2013)}.items()) + list(standard_checks(request).items()))
    context = standard_checks(request, "start")
    return render (request, "getraenkewart/index.html", context)

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate (username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            messages.success(request, "Erfolgreich eingeloggt!")
            context = standard_checks(request, "start")
            return render (request, "getraenkewart/index.html", context)
        else:
            messages.error(request, "Du bist noch nicht aktiviert! Frag mal nach.")
            context = standard_checks(request, "start")
            return render (request, "getraenkewart/index.html", context)
    else:
        messages.error(request, "Dein Passwort oder dein Benutzername ist falsch.")
        context = standard_checks(request, "start")
        return render (request, "getraenkewart/index.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, "Erfolgreich ausgeloggt!")
    context = standard_checks(request, "start")
    return render(request, "getraenkewart/index.html", context)

def register(request):
    if request.method =="GET":
        context = standard_checks(request, "start")
        return render(request, "getraenkewart/register.html", context)
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        data = {'first_name':first_name, 'last_name':last_name, 'username':username, 'password':password}
        error = False
        context = dict()
        if User.objects.filter(username__exact=username).exists():
            error = True
            context.update(dict({'username_error':True}))
            messages.error(request, "Dieser Benutzername ist bereits vergeben!")
        if first_name=="":
            error = True
            context.update(dict({'first_name_error':True}))
            messages.error(request, "Bitte gib einen Vornamen ein.")
        if last_name=="":
            error = True
            context.update(dict({'last_name_error':True}))
            messages.error(request, "Bitte gib einen Nachnamen ein.")
        if len(password) < 8:
            error = True
            context.update(dict({'password_error':True}))
            messages.error(request, "Das Passwort muss mindestens 8 Zeichen lang sein.")
        if len(username) > 30:
            error = True
            context.update(dict({'username_error':True}))
            messages.error(request, "Der Benutzername darf nicht länger als 30 Zeichen sein.")
        if len(first_name) > 30:
            error = True
            context.update(dict({'first_name_error':True}))
            messages.error(request, "Der Vorname darf nicht länger als 30 Zeichen sein.")
        if len(last_name) > 30:
            error = True
            context.update(dict({'last_name_error':True}))
            messages.error(request, "Der Nachname darf nicht länger als 30 Zeichen sein.")
        if not error:
            user = User.objects.create_user(username, "", password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = False
            user.save()
            messages.success(request, "Neuen Benutzer erfolgreich angelegt. Bitte warte auf deine Aktivierung.")
            context = standard_checks(request, "start")
            return render(request, "getraenkewart/index.html", context)
        else:
            context.update(standard_checks(request, "start"))
            context.update(data)
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

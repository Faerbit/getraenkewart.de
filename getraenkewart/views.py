from django.shortcuts import render
from getraenke.views import generate_bier_chart
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def index(request):
    context = dict(list({'chart':generate_bier_chart(2013)}.items()) + list(standard_checks(request).items()))
    return render (request, "getraenkewart/index.html", context)

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate (username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            context = standard_checks(request, "success", "Erfolgreich eingeloggt!")
            return render (request, "getraenkewart/index.html", context)
        else:
            context = standard_checks(request, "danger", "Du bist noch nicht aktiviert! Frag mal nach.")
            return render (request, "getraenkewart/index.html", context)
    else:
        context = standard_checks(request, "danger", "Dein Passwort oder dein Benutzername ist falsch.")
        return render (request, "getraenkewart/index.html", context)

def logout_view(request):
    logout(request)
    context = standard_checks(request, "success", "Erfolgreich ausgeloggt!")
    return render(request, "getraenkewart/index.html", context)

def register(request):
    if request.method =="GET":
        context = standard_checks(request)
        return render(request, "getraenkewart/register.html", context)
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        data = {'first_name':first_name, 'last_name':last_name, 'username':username, 'password':password}
        for i in User.objects.all():
            if i.username==username:
                context = dict({'username_error':True})
                context.update(standard_checks(request, "danger", "Dieser Benutzername ist bereits vergeben!"))
                context.update(data)
                return render(request, "getraenkewart/register.html", context)
        if first_name=="":
            context = dict({'first_name_error':True})
            context.update(standard_checks(request, "danger", "Bitte gib einen Vornamen ein."))
            context.update(data)
            return render(request, "getraenkewart/register.html", context)
        if len(password) < 8:
            context = dict({'password_error':True})
            context.update(standard_checks(request, "danger", "Das Passwort muss mindestens 8 Zeichen lang sein."))
            context.update(data)
            return render(request, "getraenkewart/register.html", context)
        user = User.objects.create_user(username, "", password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = False
        user.save()
        context = standard_checks(request, "success", "Neuen Benutzer erfolgreich angelegt. Bitte warte auf deine Aktivierung.")
        return render(request, "getraenkewart/index.html", context)

def standard_checks(request, alert_type="", alert_message=""):
    if request.user.is_authenticated():
        name = request.user.first_name
    else:
        name = ""
    if alert_type == "":
        return {'name':name, 'alert_type':"", 'alert_message':""}
    else:
        return {'name':name, 'alert_type':alert_type, 'alert_message':alert_message}

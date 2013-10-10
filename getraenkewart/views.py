from django.shortcuts import render
from getraenke.views import generate_bier_chart
from django.contrib.auth import authenticate, login, logout

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

def standard_checks(request, alert_type="", alert_message=""):
    if request.user.is_authenticated():
        name = request.user.first_name
    else:
        name = ""
    if alert_type == "":
        return {'name':name, 'alert_type':"", 'alert_message':""}
    else:
        return {'name':name, 'alert_type':alert_type, 'alert_message':alert_message}

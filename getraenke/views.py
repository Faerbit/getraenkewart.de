from django.shortcuts import render, redirect
from datetime import date
from django.contrib import messages
from django.contrib.auth.models import User

from getraenke.models import Person, Jahr, Monat

def generate_bier_chart (year):
	#xdata = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
	"""xdata = []
	for i in range(1,13):
		xdata.append(i)"""
	xdata = []
	for i in range(1, 13):
		xdata.append(date(year, i, 1))
	chartdata = { 'x' : xdata}
	count = 0
	for i in Person.objects.all():
		count += 1
		for j in i.jahre.all():
			if (j.jahr == year):
				ydata = [j.januar.bierstriche, j.februar.bierstriche, j.maerz.bierstriche,
					j.april.bierstriche, j.mai.bierstriche, j.juni.bierstriche,j.juli.bierstriche, j.august.bierstriche, 
					j.september.bierstriche, j.oktober.bierstriche, j.november.bierstriche, j.dezember.bierstriche]
				chartdata['name' + str(count)] = str(i)
				chartdata['y' + str(count)] = ydata
				#extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
				#chartdata['extra' + str(count)] = extra_serie
	charttype = "lineChart"
	data = {
			'charttype': charttype,
			'charttdata': chartdata
			}
	return data

def people(request):
    if request.method == "POST":
        pass
    new_registrations = User.objects.filter(is_active__exact=False)
    unlinked_persons = Person.objects.filter(user__exact=-1)
    linked_persons = Person.objects.exclude(user__exact=-1)
    return render (request, "getraenke/people.html", {
            "new_registrations": new_registrations,
            "unlinked_persons": unlinked_persons,
            "linked_persons": linked_persons,
        })

def highscore(request, year=None):
    if not request.user.is_authenticated():
        messages.error(request, "Du musst dich erst einloggen.")
        return redirect("/")
    if year == None:
        year = date.today().year
    year = int(year)
    context = {'year':year, 'year_previous':year-1, 'year_next':year+1}
    personen = []
    empty = True
    for i in Person.objects.filter(jahre__jahr__exact=year):
        empty = False
        j = i.jahre.get(jahr=year)
        jan = j.januar.bierstriche
        feb = j.februar.bierstriche
        mar = j.maerz.bierstriche
        apr = j.april.bierstriche
        mai = j.mai.bierstriche
        jun = j.juni.bierstriche
        jul = j.juli.bierstriche
        aug = j.august.bierstriche
        sep = j.september.bierstriche
        okt = j.oktober.bierstriche
        nov = j.november.bierstriche
        dez = j.dezember.bierstriche
        summe = jan + feb + mar + apr + mai + jun + jul + aug + sep + okt + nov + dez
        personen.append([i.name, summe, jan, feb, mar, apr, mai, jun, jul, aug, sep, okt, nov, dez])
        personen.sort(key= lambda x:x[1], reverse=True)
    if not empty:
        context.update({'personen':personen})
    else:
        context.update({'empty':True})
    return render (request, "getraenke/highscore.html", context)

def manage(request, year=None, month=None):
    if not request.user.is_authenticated():
        messages.error(request, "Du musst dich erst einloggen.")
        return redirect("/")
    elif not request.user.is_staff:
        messages.error(request, "Zugriff verweigert!")
        return redirect("/")
    if year == None:
        year = date.today().year
    year = int(year)
    context = {'year':year, 'year_previous':year-1, 'year_next':year+1}
    if month == None:
        month = date.today().month
    month = int(month)
    context.update({'month':month})
    if month == 1:
        context.update({'month_previous':12, 'month_next':2})
    elif month == 12:
        context.update({'month_previous':11, 'month_next':1})
    else:
        context.update({'month_previous':month-1, 'month_next':month+1})
    context.update({"url":request.path})
    if request.method == "POST":
        if "new-year" in request.POST:
            for i in Person.objects.all():
                if i.name + "-check" in request.POST:
                    i.add_year(year)
        else:
            for i in Person.objects.filter(jahre__jahr__exact=year):
                try:
                    bier = int(request.POST[i.name + "-bier"])
                except ValueError:
                    bier = 0
                try:
                    cola = int(request.POST[i.name + "-cola"])
                except ValueError:
                    cola = 0
                try:
                    geld = int(request.POST[i.name + "-geld"])
                except ValueError:
                    geld = 0
                j = i.jahre.get(jahr=year)
                if month == 1:
                    j.januar.bierstriche += bier
                    j.januar.colastriche += cola
                    j.januar.bezahlt += geld
                    j.januar.save()
                if month == 2:
                    j.februar.bierstriche += bier
                    j.februar.colastriche += cola
                    j.februar.bezahlt += geld
                    j.februar.save()
                if month == 3:
                    j.maerz.bierstriche += bier
                    j.maerz.colastriche += cola
                    j.maerz.bezahlt += geld
                    j.maerz.save()
                if month == 4:
                    j.april.bierstriche += bier
                    j.april.colastriche += cola
                    j.april.bezahlt += geld
                    j.april.save()
                if month == 5:
                    j.mai.bierstriche += bier
                    j.mai.colastriche += cola
                    j.mai.bezahlt += geld
                    j.mai.save()
                if month == 6:
                    j.juni.bierstriche += bier
                    j.juni.colastriche += cola
                    j.juni.bezahlt += geld
                    j.juni.save()
                if month == 7:
                    j.juli.bierstriche += bier
                    j.juli.colastriche += cola
                    j.juli.bezahlt += geld
                    j.juli.save()
                if month == 8:
                    j.august.bierstriche += bier
                    j.august.colastriche += cola
                    j.august.bezahlt += geld
                    j.august.save()
                if month == 9:
                    j.september.bierstriche += bier
                    j.september.colastriche += cola
                    j.september.bezahlt += geld
                    j.september.save()
                if month == 10:
                    j.oktober.bierstriche += bier
                    j.oktober.colastriche += cola
                    j.oktober.bezahlt += geld
                    j.oktober.save()
                if month == 11:
                    j.november.bierstriche += bier
                    j.november.colastriche += cola
                    j.november.bezahlt += geld
                    j.november.save()
                if month == 12:
                    j.dezember.bierstriche += bier
                    j.dezember.colastriche += cola
                    j.dezember.bezahlt += geld
                    j.dezember.save()
            if request.POST["new-name"] != "":
                if Person.objects.filter(name=request.POST["new-name"]).exists():
                    messages.error(request, "Namen dürfen nicht doppelt vorkommen.")
                else:
                    person = Person(name=request.POST["new-name"])
                    person.save()
                    person.add_year(year)
            if request.POST["data-input"] != "":
                person = Person.objects.get(name=request.POST["data-input"])
                person.jahre.get(jahr=year).delete()
                if not person.jahre.exists():
                    person.delete()

    persObjects = Person.objects.filter(jahre__jahr__exact=year)
    personen = []
    empty = True
    if not Person.objects.exists():
        empty = False
    if not persObjects.exists():
        prevPersObjects = Person.objects.filter(jahre__jahr__exact=year-1)
        for i in Person.objects.all():
            if i in prevPersObjects:
                personen.append([i.name, True])
            else:
                personen.append([i.name, False])
            
    for i in persObjects:
        empty = False
        j = i.jahre.get(jahr=year)
        if month == 1:
            bier = j.januar.bierstriche
            cola = j.januar.colastriche
            bezahlt = j.januar.bezahlt
        if month == 2:
            bier = j.februar.bierstriche
            cola = j.februar.colastriche
            bezahlt = j.februar.bezahlt
        if month == 3:
            bier = j.maerz.bierstriche
            cola = j.maerz.colastriche
            bezahlt = j.maerz.bezahlt
        if month == 4:
            bier = j.april.bierstriche
            cola = j.april.colastriche
            bezahlt = j.april.bezahlt
        if month == 5:
            bier = j.mai.bierstriche
            cola = j.mai.colastriche
            bezahlt = j.mai.bezahlt
        if month == 6:
            bier = j.juni.bierstriche
            cola = j.juni.colastriche
            bezahlt = j.juni.bezahlt
        if month == 7:
            bier = j.juli.bierstriche
            cola = j.juli.colastriche
            bezahlt = j.juli.bezahlt
        if month == 8:
            bier = j.august.bierstriche
            cola = j.august.colastriche
            bezahlt = j.august.bezahlt
        if month == 9:
            bier = j.september.bierstriche
            cola = j.september.colastriche
            bezahlt = j.september.bezahlt
        if month == 10:
            bier = j.oktober.bierstriche
            cola = j.oktober.colastriche
            bezahlt = j.oktober.bezahlt
        if month == 11:
            bier = j.november.bierstriche
            cola = j.november.colastriche
            bezahlt = j.november.bezahlt
        if month == 12:
            bier = j.dezember.bierstriche
            cola = j.dezember.colastriche
            bezahlt = j.dezember.bezahlt
        personen.append([i.name, bier, cola, bezahlt])
    if empty:
        context.update({'empty':True})
        context.update({'personen':personen})
    else:
        context.update({'personen':personen})
    return render (request, "getraenke/manage.html", context)

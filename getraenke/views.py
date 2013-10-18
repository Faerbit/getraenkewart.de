from django.shortcuts import render
from getraenke.models import Person, Jahr, Monat
from  getraenkewart.views import standard_checks
from datetime import date
#import pdb

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

def highscore(request, year=None):
    if year == None:
        year = date.today().year
    year = int(year)
    context = {'year':year, 'year_previous':year-1, 'year_next':year+1}
    empty = False
    personen = []
    for i in Person.objects.all():  #TODO: change to direct query with year and handle exception also figure the table template out
        j = i.jahre.get(jahr=year)
        if not j == None:
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
    if not empty:
        context.update({'personen':personen})
    else:
        context.update({'empty':True})
    context.update(standard_checks(request, "getraenke"))
    return render (request, "getraenke/highscore.html", context)


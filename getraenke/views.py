from django.shortcuts import render
from getraenke.models import Person, Jahr, Monat
from  getraenkewart.views import standard_checks
from datetime import date

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

def highscore(request):
    context = standard_checks(request, "getraenke")
    return render (request, "getraenke/highscore.html", context)


from django.db import models

class Person(models.Model):
	name = models.CharField(max_length=50)
	jahr_ids = models.TextField(default="")
	
	def add_year(self, jahr):
		jan, feb, mae, apr, mai, jun, jul, aug, sep, okt, nov, dez = Monat(), Monat(), Monat(), Monat(), Monat(), Monat(), Monat(), Monat(), Monat(), Monat(), Monat(), Monat()
		for i in [jan, feb, mae, apr, mai, jun, jul, aug, sep, okt, nov, dez]:
			#i = Monat()
			i.save()
		neues_jahr = Jahr(jahr = jahr, januar = jan, februar = feb, maerz = mae, april = apr, mai = mai, juni = jun, juli = jul, august = aug, september = sep, oktober= okt, november = nov, dezember = dez)
		neues_jahr.save()
		self.jahr_ids += str(neues_jahr.id) + ";"
		self.save()

	def __str__(self):
		return self.name

class Monat (models.Model):
	bierstriche = models.IntegerField(default=0)
	colasnacktriche = models.IntegerField(default=0)
	#snackstriche = models.IntegerField(default=0)
	bezahlt = models.IntegerField(default=0)

	def add_monat():
		m = Monat()
		m.save()
		return m

class Jahr(models.Model):
	#person = models.ForeignKey(Person)
	sonstige_kosten = models.IntegerField(default=0)
	bemerkung = models.TextField()
	jahr = models.IntegerField()
	januar = models.ForeignKey(Monat, related_name = "+")
	februar = models.ForeignKey(Monat, related_name = "+")
	maerz  = models.ForeignKey(Monat, related_name = "+")
	april = models.ForeignKey(Monat, related_name = "+")
	mai  = models.ForeignKey(Monat, related_name = "+")
	juni  = models.ForeignKey(Monat, related_name = "+")
	juli  = models.ForeignKey(Monat, related_name = "+")
	august  = models.ForeignKey(Monat, related_name = "+")
	september  = models.ForeignKey(Monat, related_name = "+")
	oktober  = models.ForeignKey(Monat, related_name = "+")
	november  = models.ForeignKey(Monat, related_name = "+")
	dezember  = models.ForeignKey(Monat, related_name = "+")

	def __str__(self):
		return str(self.jahr)

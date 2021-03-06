from django.db import models
from django.contrib.auth.models import User

class Monat (models.Model):
    bierstriche = models.IntegerField(default=0)
    colastriche = models.IntegerField(default=0)
    bezahlt = models.IntegerField(default=0)

class Jahr(models.Model):
    sonstige_kosten = models.IntegerField(default=0)
    bemerkung = models.TextField()
    jahr = models.IntegerField()
    #januar = models.ForeignKey(Monat, related_name = "+") 
    #februar = models.ForeignKey(Monat, related_name = "+")
    #maerz  = models.ForeignKey(Monat, related_name = "+")
    #april = models.ForeignKey(Monat, related_name = "+")
    #mai  = models.ForeignKey(Monat, related_name = "+")
    #juni  = models.ForeignKey(Monat, related_name = "+")
    #juli  = models.ForeignKey(Monat, related_name = "+")
    #august  = models.ForeignKey(Monat, related_name = "+")
    #september  = models.ForeignKey(Monat, related_name = "+")
    #oktober  = models.ForeignKey(Monat, related_name = "+")
    #november  = models.ForeignKey(Monat, related_name = "+")
    #dezember  = models.ForeignKey(Monat, related_name = "+")

    def __str__(self):
            return str(self.jahr)

class Person(models.Model):
    # support full range of user object names
    name = models.CharField(max_length=61, unique=True)
    # assign to nobody per default
    user = models.ForeignKey (User, default=-1)
    jahre = models.ManyToManyField(Jahr)

    def __str__(self):
            return self.name

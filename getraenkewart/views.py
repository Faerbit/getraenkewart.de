from django.shortcuts import render
from getraenke.views import generate_bier_chart

def index(request):
	return render (request, "getraenkewart/index.html", generate_bier_chart(2013))

from django.shortcuts import render
from django.http import HttpResponse
from django.apps import apps
import os
from django.template import loader

from .models import Person

# Create your views here.

TRIGGER = False

def index(request):
	# acc = ""
	# for app_config in apps.get_app_configs():
	# 	acc = acc + " \n" + app_config.name
	# if not TRIGGER:
	# 	return HttpResponse(acc)
	# else:
	# 	return HttpResponse("TRIGGERED!!!!")
	name_list = Person.objects.all()
	context = {'People': name_list}
	return render(request, 'AlexaHandler/list.html', context)

def live(request):
	context = {'Title': "Live Alexa"}
	return render(request, 'AlexaHandler/live.html', context)

def setVar(request, var):
	return HttpResponse(var)

def trigger():
	print("Triggered")
	TRIGGER = True
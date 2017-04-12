from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Person

# Create your views here.

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

@login_required(login_url='/login/')
def live(request):
	context = {'Title': "Live Alexa"}
	return render(request, 'AlexaHandler/live.html', context)

@login_required(login_url='/login/')
def serve_cache(request):
	print("File_Request: ", request.path.split("cache", 1)[1])
	file = request.path.split("cache", 1)[1]
	path = settings.CACHE_DIR + file
	print("SERVE PATH: ", path)
	image_data = open(path, "rb").read()
	return HttpResponse(image_data, content_type="image/png")
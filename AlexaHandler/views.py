from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Person
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login/')
def live(request):
	context = {'Title': "Live Alexa",
				'SOCKET': settings.SOCKET_URL}
	return render(request, 'AlexaHandler/live.html', context)

@login_required(login_url='/login/')
def serve_cache(request):
	print("File_Request: ", request.path.split("cache", 1)[1])
	file = request.path.split("cache", 1)[1]
	path = settings.CACHE_DIR + file
	print("SERVE PATH: ", path)
	image_data = open(path, "rb").read()
	return HttpResponse(image_data, content_type="image/png")
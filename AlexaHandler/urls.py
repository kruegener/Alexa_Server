from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.live, name='index'),
	url(r'^live/', views.live, name='live'),
	url(r'^cache/', views.serve_cache, name='serve_cache'),
	]
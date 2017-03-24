from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^live/', views.live, name='index'),
	url(r'([0-9]+)', views.setVar, name='setVar')
	]
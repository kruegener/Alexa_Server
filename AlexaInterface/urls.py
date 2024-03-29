"""AlexaInterface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
import AlexaHandler


urlpatterns = [

	url(r'^AlexaHandler/', include('AlexaHandler.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', AlexaHandler.views.live, name="live"),
    url(r'^login/$', auth_views.login, {'template_name': 'AlexaHandler/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^live/', AlexaHandler.views.live, name='live'),
    url(r'^', include('django_alexa.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

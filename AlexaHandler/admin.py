from django.contrib import admin

# Register your models here.

from .models import Person
from .models import File

admin.site.register(Person)
admin.site.register(File)
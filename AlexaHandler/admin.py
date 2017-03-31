from django.contrib import admin

# Register your models here.

from .models import Person
from .models import File
from .models import ClientSession
from .models import SessionVar
from .models import SessionVarFile
from .models import SessionFile
from .models import Node
from .models import NodeFlow

admin.site.register(Person)
admin.site.register(File)
admin.site.register(ClientSession)
admin.site.register(NodeFlow)
admin.site.register(Node)
admin.site.register(SessionVar)
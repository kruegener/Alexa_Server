from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Person)
admin.site.register(File)
admin.site.register(ClientSession)
admin.site.register(NodeFlow)
admin.site.register(Node)
admin.site.register(SessionVar)
admin.site.register(BlockChainModel)
admin.site.register(BlockModel)
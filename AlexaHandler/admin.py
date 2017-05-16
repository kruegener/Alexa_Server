from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Person)
admin.site.register(File)
#admin.site.register(ClientSession)
#admin.site.register(NodeFlow)
#admin.site.register(Node)
#admin.site.register(SessionVar)
admin.site.register(BlockChainModel)
admin.site.register(BlockModel)

class CacheTableAdmin(admin.ModelAdmin):
    list_display = ('cache_key', 'expires')
    search_fields = ('cache_key', )

admin.site.register(CacheTable, CacheTableAdmin)
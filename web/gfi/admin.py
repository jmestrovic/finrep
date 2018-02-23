from django.contrib import admin
from .models import Companies
from .models import ListItems
from .models import GfiHeaders
from .models import GfiDetails

class CompaniesAdmin(admin.ModelAdmin):
    list_display = ('abbreviation', 'name',)

admin.site.register(Companies, CompaniesAdmin)
admin.site.register(ListItems)
admin.site.register(GfiHeaders)
admin.site.register(GfiDetails)

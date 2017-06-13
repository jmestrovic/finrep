from django.contrib import admin
from .models import Companies
from .models import ListItems
from .models import GfiHeaders
from .models import GfiDetails

admin.site.register(Companies)
admin.site.register(ListItems)
admin.site.register(GfiHeaders)
admin.site.register(GfiDetails)

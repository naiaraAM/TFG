# pages/admin.py

from django.contrib import admin
from .models import Samples, Comparison

class PageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Samples, PageAdmin)
admin.site.register(Comparison, PageAdmin)
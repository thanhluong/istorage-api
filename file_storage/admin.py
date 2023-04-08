from django.contrib import admin
from .models import Document, GovFile


class DocumentAdmin(admin.ModelAdmin):
    pass


class GovFileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Document)
admin.site.register(GovFile)

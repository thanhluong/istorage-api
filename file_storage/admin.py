from django.contrib import admin
from .models import Document, GovFile, GovFileProfile
from .models import SiteMenu
from .models import OrganTemplate


class DocumentAdmin(admin.ModelAdmin):
    pass


class GovFileAdmin(admin.ModelAdmin):
    pass


class SiteMenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_id')


class OrganTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'organ_name')


admin.site.register(Document)
admin.site.register(GovFile)
admin.site.register(GovFileProfile)
admin.site.register(SiteMenu, SiteMenuAdmin)
admin.site.register(OrganTemplate, OrganTemplateAdmin)

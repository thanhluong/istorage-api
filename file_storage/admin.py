from django.contrib import admin
from .models import Document, GovFile, GovFileProfile
from .models import SiteMenu
from .models import OrganTemplate
from .models import DocumentSecurityLevel
from .models import OrganRole
from .models import Organ


class DocumentAdmin(admin.ModelAdmin):
    pass


class GovFileAdmin(admin.ModelAdmin):
    pass


class SiteMenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_id')


class OrganTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'organ_name')


class DocumentSecurityLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class OrganRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class OrganAdmin(admin.ModelAdmin):
    list_display = ('name', 'districtName', 'wardName')


admin.site.register(Document)
admin.site.register(GovFile)
admin.site.register(GovFileProfile)
admin.site.register(SiteMenu, SiteMenuAdmin)
admin.site.register(OrganTemplate, OrganTemplateAdmin)
admin.site.register(DocumentSecurityLevel, DocumentSecurityLevelAdmin)
admin.site.register(OrganRole, OrganRoleAdmin)
admin.site.register(Organ, OrganAdmin)

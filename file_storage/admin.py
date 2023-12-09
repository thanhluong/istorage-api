from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import StorageUser
from .models import Document, GovFile, GovFileProfile
from .models import SiteMenu
from .models import OrganTemplate
from .models import DocumentSecurityLevel
from .models import OrganRole
from .models import Organ, OrganDepartment
from .models import Phong


class StorageUserAdmin(UserAdmin):
    list_display = ('full_name', 'username', 'email', 'is_active', 'is_staff')
    readonly_fields = ('date_joined', 'last_login', 'menu_permission')

    fieldsets = [
        ('Thông tin cá nhân', {'fields': ['full_name', 'phone', 'email']}),
        ('Thông tin đăng nhập', {'fields': ['username', 'password']}),
        ('Thông tin cơ quan', {'fields': ['department', 'role']}),
        ('Thông tin quyền hạn', {'fields': ['is_active', 'is_staff', 'is_archive_staff', 'is_superuser']}),
        ('Thông tin hệ thống', {'fields': ['date_joined', 'last_login']}),
    ]

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
    list_display = ('name', 'organ', 'description')


class OrganAdmin(admin.ModelAdmin):
    list_display = ('name', 'districtName', 'wardName')


class OrganDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'organ')


class PhongAdmin(admin.ModelAdmin):
    list_display = ('fond_name', 'organ')


admin.site.register(StorageUser, StorageUserAdmin)
admin.site.register(Document)
admin.site.register(GovFile)
admin.site.register(GovFileProfile)
admin.site.register(SiteMenu, SiteMenuAdmin)
admin.site.register(OrganTemplate, OrganTemplateAdmin)
admin.site.register(DocumentSecurityLevel, DocumentSecurityLevelAdmin)
admin.site.register(OrganRole, OrganRoleAdmin)
admin.site.register(Organ, OrganAdmin)
admin.site.register(OrganDepartment, OrganDepartmentAdmin)
admin.site.register(Phong, PhongAdmin)
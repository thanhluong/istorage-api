from rest_framework import serializers

from file_storage.models import StorageUser
from file_storage.models import Document, GovFile, GovFileProfile
from file_storage.models import Organ, OrganDepartment, OrganRole
from file_storage.models import Phong, CategoryFile
from file_storage.models import GovFileLanguage, StorageDuration, PhysicalState
from file_storage.models import Plan
from file_storage.models import Warehouse, WarehouseRoom, Drawer, Shelf


class StorageUserSerializer(serializers.ModelSerializer):
    organ_id = serializers.SerializerMethodField()
    organ_name = serializers.SerializerMethodField()

    class Meta:
        model = StorageUser
        exclude = ('password',)

    def get_organ_id(self, obj):
        if obj.department:
            if obj.department.organ:
                return obj.department.organ.id
            return ""
        return ""

    def get_organ_name(self, obj):
        if obj.department:
            if obj.department.organ:
                return obj.department.organ.name
            return ""
        return ""


class StorageUserCreationSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        user = StorageUser(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            full_name=self.validated_data['full_name'],
            phone=self.validated_data['phone'],
            is_staff=self.validated_data['is_staff'],
            role=self.validated_data['role'],
            department=self.validated_data['department'],
            menu_permission=self.validated_data['menu_permission'],
            is_superuser=False,
            is_active=True,
            is_archive_staff=False,
            first_name="",
            last_name=""
        )
        print(self.data)
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = StorageUser
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    def save_file(self, file, file_path):
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return file_path


class PhongSerializer(serializers.ModelSerializer):
    organ = serializers.PrimaryKeyRelatedField(queryset=Organ.objects.all())

    class Meta:
        model = Phong
        fields = '__all__'


class CategoryFileSerializer(serializers.ModelSerializer):
    organ = serializers.PrimaryKeyRelatedField(queryset=Organ.objects.all())
    parent = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=CategoryFile.objects.all())

    class Meta:
        model = CategoryFile
        fields = '__all__'


class GovFileSerializer(serializers.ModelSerializer):
    identifier = serializers.PrimaryKeyRelatedField(queryset=Organ.objects.all())
    organ_id = serializers.PrimaryKeyRelatedField(queryset=Phong.objects.all())
    category_file = serializers.PrimaryKeyRelatedField(queryset=CategoryFile.objects.all())
    format = serializers.PrimaryKeyRelatedField(queryset=PhysicalState.objects.all())
    language = serializers.PrimaryKeyRelatedField(queryset=GovFileLanguage.objects.all())
    maintenance = serializers.PrimaryKeyRelatedField(queryset=StorageDuration.objects.all())

    plan_thuthap = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=Plan.objects.all())
    plan_bmcl = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=Plan.objects.all())
    plan_nopluuls = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=Plan.objects.all())
    plan_tieuhuy = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=Plan.objects.all())

    drawer = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=Drawer.objects.all())

    organ_id_name = serializers.SerializerMethodField()
    maintenance_name = serializers.SerializerMethodField()
    drawer_name = serializers.SerializerMethodField()

    class Meta:
        model = GovFile
        fields = '__all__'

    def get_organ_id_name(self, obj):
        if obj.organ_id:
            return obj.organ_id.fond_name
        return ""

    def get_maintenance_name(self, obj):
        if obj.maintenance:
            return obj.maintenance.duration
        return ""

    def get_drawer_name(self, obj):
        if obj.drawer:
            result = obj.drawer.name
            if obj.drawer.shelf:
                result = obj.drawer.shelf.name + ", " + result
                if obj.drawer.shelf.warehouse_room:
                    result = obj.drawer.shelf.warehouse_room.name + ", " + result
                    if obj.drawer.shelf.warehouse_room.warehouse:
                        result = obj.drawer.shelf.warehouse_room.warehouse.name + ", " + result
            return result
        return ""


class GovFileProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovFileProfile
        fields = '__all__'


class OrganSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organ
        fields = '__all__'


class OrganDepartmentSerializer(serializers.ModelSerializer):
    organ = serializers.PrimaryKeyRelatedField(queryset=Organ.objects.all())

    class Meta:
        model = OrganDepartment
        fields = '__all__'


class OrganRoleSerializer(serializers.ModelSerializer):
    organ = serializers.PrimaryKeyRelatedField(queryset=Organ.objects.all())

    class Meta:
        model = OrganRole
        fields = '__all__'


class GovFileLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovFileLanguage
        fields = '__all__'


class StorageDurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageDuration
        fields = '__all__'


class PhysicalStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalState
        fields = '__all__'


class PlanSerializer(serializers.ModelSerializer):
    organ = serializers.PrimaryKeyRelatedField(queryset=Organ.objects.all())
    attachment = serializers.FileField(required=False, allow_null=True)

    organ_name = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = '__all__'

    def get_organ_name(self, obj):
        if obj.organ:
            return obj.organ.name
        return ""


class WarehouseSerializer(serializers.ModelSerializer):
    organ = serializers.PrimaryKeyRelatedField(queryset=Organ.objects.all())

    organ_name = serializers.SerializerMethodField()

    class Meta:
        model = Warehouse
        fields = '__all__'

    def get_organ_name(self, obj):
        if obj.organ:
            return obj.organ.name
        return ""


class WarehouseRoomSerializer(serializers.ModelSerializer):
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())

    class Meta:
        model = WarehouseRoom
        fields = '__all__'


class ShelfSerializer(serializers.ModelSerializer):
    warehouse_room = serializers.PrimaryKeyRelatedField(queryset=WarehouseRoom.objects.all())

    class Meta:
        model = Shelf
        fields = '__all__'


class DrawerSerializer(serializers.ModelSerializer):
    shelf = serializers.PrimaryKeyRelatedField(queryset=Shelf.objects.all())

    class Meta:
        model = Drawer
        fields = '__all__'
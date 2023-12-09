from rest_framework import serializers

from file_storage.models import StorageUser
from file_storage.models import Document, GovFile, GovFileProfile
from file_storage.models import Organ, OrganDepartment
from file_storage.models import Phong, CategoryFile


class StorageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageUser
        exclude = ('password',)


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
    parent = serializers.PrimaryKeyRelatedField(queryset=CategoryFile.objects.all())

    class Meta:
        model = CategoryFile
        fields = '__all__'


class GovFileSerializer(serializers.ModelSerializer):
    official_organ = serializers.PrimaryKeyRelatedField(queryset=Organ.objects.all())
    organ_id = serializers.PrimaryKeyRelatedField(queryset=Phong.objects.all())

    class Meta:
        model = GovFile
        fields = '__all__'


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
    class Meta:
        model = OrganDepartment
        fields = '__all__'

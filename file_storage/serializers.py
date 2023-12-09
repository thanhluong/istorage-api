from rest_framework import serializers
from file_storage.models import Document, GovFile, GovFileProfile
from file_storage.models import Organ, OrganDepartment
from file_storage.models import Phong


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    def save_file(self, file, file_path):
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return file_path


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

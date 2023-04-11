from rest_framework import serializers
from file_storage.models import Document, GovFile, GovFileProfile


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
    class Meta:
        model = GovFile
        fields = '__all__'


class GovFileProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovFileProfile
        fields = '__all__'

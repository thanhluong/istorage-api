from abc import ABC

from rest_framework import serializers
import os
from django.conf import settings
from file_storage.models import Document


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('file_id', 'issued_date', 'autograph', 'code_number', 'document_path', 'file_name')

    def save_file(self, file, file_path):
        # destination_folder = os.path.join(settings.STATIC_ROOT, settings.STATIC_PATH)
        # destination_path = os.path.join(destination_folder, file_name)

        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return file_path


class GovFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('file_id',)

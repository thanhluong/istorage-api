from rest_framework import serializers
from file_storage.models import Document, GovFile


class DocumentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        data = kwargs.get('data', None)
        is_partial = kwargs.get('partial', False)
        super().__init__(*args, **kwargs)

        if data or is_partial:
            # Get field names from the data dictionary (assuming it's a flat dictionary)
            field_names = list(data.keys()) if data else []

            # Set the instance's fields to the ones in the data dictionary
            allowed_fields = set(field_names)
        else:
            # If we are serializing (i.e., data is not present in kwargs), use a specific set of fields
            allowed_fields = {'id', 'gov_file_id', 'doc_ordinal', 'issued_date', 'autograph', 'code_number', 'doc_name'}

        # Remove fields that are not in the allowed_fields set
        for field_name in set(self.fields.keys()):
            if field_name not in allowed_fields:
                self.fields.pop(field_name)

    class Meta:
        model = Document
        fields = '__all__'

    def save_file(self, file, file_path):
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return file_path


class GovFileSerializer(serializers.ModelSerializer):
    # def __init__(self, *args, **kwargs):
    #     data = kwargs.get('data', None)
    #     is_partial = kwargs.get('partial', False)
    #     super().__init__(*args, **kwargs)
    #
    #     if data or is_partial:
    #         # Get field names from the data dictionary (assuming it's a flat dictionary)
    #         field_names = list(data.keys()) if data else []
    #
    #         # Set the instance's fields to the ones in the data dictionary
    #         allowed_fields = set(field_names)
    #     else:
    #         # If we are serializing (i.e., data is not present in kwargs), use a specific set of fields
    #         allowed_fields = '__all__'
    #
    #     # Remove fields that are not in the allowed_fields set
    #     for field_name in set(self.fields.keys()):
    #         if field_name not in allowed_fields:
    #             self.fields.pop(field_name)

    class Meta:
        model = GovFile
        fields = '__all__'

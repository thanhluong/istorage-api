from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from .models import Document, GovFile
from .serializers import DocumentUploadSerializer, GovFileSerializer

import os
import hashlib


def md5_file(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class DocumentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"file": ["No file was submitted."]}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        folder_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT,
                                   settings.DOCUMENT_PATH, request.data['file_id'])
        if not os.path.isdir(folder_path):
            os.system('mkdir ' + folder_path)
        file_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT,
                                 settings.DOCUMENT_PATH, request.data['file_id'],
                                 file.name)

        doc_table_data = {
            'file_id': request.data.get('file_id', ''),
            'issued_date': request.data.get('issued_date', ''),
            'autograph': request.data.get('autograph', ''),
            'code_number': request.data.get('code_number', ''),
            'document_path': file_path,
            'file_name': file.name,
        }
        serializer = DocumentUploadSerializer(data=doc_table_data)
        serializer.save_file(file, file_path)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetDocumentByFileId(APIView):
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        file_id = request.GET.get('file_id')
        if file_id:
            docs = Document.objects.filter(file_id=file_id)
            serializer = DocumentUploadSerializer(docs, many=True)
            serialization_result = serializer.data
            result = []
            for doc in serialization_result:
                doc['url'] = "http://" + request.get_host()  \
                            + "/" + settings.MEDIA_ROOT + "/" + settings.DOCUMENT_PATH \
                            + "/" + doc['file_id'] + "/" + doc['file_name']
                result.append(doc)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Missing file_storage_id parameter'}, status=status.HTTP_400_BAD_REQUEST)


class GetFiles(APIView):
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        docs = GovFile.objects.all()
        serializer = GovFileSerializer(docs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

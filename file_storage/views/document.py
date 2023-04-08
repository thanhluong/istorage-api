from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.conf import settings
from django.shortcuts import get_object_or_404

from file_storage.models import Document
from file_storage.serializers import DocumentSerializer

import os


class DocumentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"file": ["No file was submitted."]}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        folder_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT,
                                   settings.DOCUMENT_PATH, request.data['gov_file_id'])

        if not os.path.isdir(folder_path):
            os.system('mkdir -p ' + folder_path)
        file_path = os.path.join(folder_path, file.name)

        doc_table_data = {
            'doc_name': file.name,
        }
        doc_table_data.update(dict(request.data.items()))

        serializer = DocumentSerializer(data=doc_table_data)
        serializer.save_file(file, file_path)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetDocumentByGovFileId(APIView):
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        gov_file_id = request.GET.get('gov_file_id')
        if gov_file_id:
            docs = Document.objects.filter(gov_file_id=gov_file_id)
            serializer = DocumentSerializer(docs, many=True)
            serialization_result = serializer.data
            result = []
            for doc in serialization_result:
                doc['url'] = os.path.join("http://", request.get_host(),
                                          settings.MEDIA_ROOT, settings.DOCUMENT_PATH,
                                          doc['gov_file_id'], doc['doc_name'])
                result.append(doc)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Missing file_id parameter'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteDocumentById(APIView):
    def delete(self, request):
        document_id = request.GET.get('document_id')
        document = get_object_or_404(Document, id=document_id)
        document.delete()
        return Response(status=status.HTTP_200_OK)


class UpdateDocumentById(APIView):
    def patch(self, request):
        document_id = request.GET.get('document_id')
        document = get_object_or_404(Document, id=document_id)
        serializer = DocumentSerializer(instance=document, data=dict(request.data.items()), partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

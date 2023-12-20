from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from file_storage.models import Document
from file_storage.serializers import DocumentSerializer

import os

from pymongo import MongoClient
from pypdf import PdfReader 


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class DocumentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongo_client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        self.mongo_collection = self.mongo_client[settings.MONGO_DB_NAME][settings.MONGO_FTS_COLLECTION_NAME]

    def insert_to_fts_db(
            self,
            file_path,
            gov_file_id, 
            doc_id,
            doc_code,
            doc_name
            ):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            page_text = page_text.replace("\n", " ")
            text += page_text
        new_doc = {
            "gov_file_id": gov_file_id,
            "doc_id": doc_id,
            "text": text,
            "doc_code": doc_code,
            "doc_name": doc_name
        }
        self.mongo_collection.insert_one(new_doc)
        return 0


    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            response_msg = {
                "error_code": status.HTTP_400_BAD_REQUEST,
                "description": "Không có văn bản nào được đính kèm"
            }
            return Response(response_msg, status=status.HTTP_200_OK)

        file = request.FILES['file']
        folder_path = str(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT,
                                   settings.DOCUMENT_PATH, request.data['gov_file_id']))

        if not os.path.isdir(folder_path):
            os.system('mkdir -p ' + folder_path)

        filename = file.name

        if 'doc_name' in request.data and len(request.data['doc_name'].strip()) > 0:
            filename = request.data['doc_name'].strip()

        if not filename.endswith('.pdf'):
            filename += '.pdf'

        file_path = os.path.join(folder_path, filename)

        doc_table_data = {
            'doc_name': filename,
        }
        doc_table_data.update(dict(request.data.items()))

        serializer = DocumentSerializer(data=doc_table_data)
        serializer.save_file(file, file_path)

        if serializer.is_valid():
            serializer.save()
            try:
                self.insert_to_fts_db(
                    file_path=file_path,
                    gov_file_id=serializer.data["gov_file_id"],
                    doc_id=serializer.data["id"],
                    doc_code=serializer.data["doc_code"],
                    doc_name=filename
                )
            except:
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        response_msg = {
            "error_code": status.HTTP_400_BAD_REQUEST,
            "description": "Invalid data"
        }
        return Response(response_msg, status=status.HTTP_200_OK)


class GetDocumentByGovFileId(APIView):
    parser_classes = [JSONParser]
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request, *args, **kwargs):
        gov_file_id = request.GET.get('gov_file_id')
        if gov_file_id:
            docs = Document.objects.filter(gov_file_id=gov_file_id)
            serializer = DocumentSerializer(docs, many=True)
            serialization_result = serializer.data
            result = []
            for doc in serialization_result:
                doc['url'] = "https://" + request.get_host() + '/api/display_pdf' \
                              + '/' + doc['gov_file_id'] + '/' + str(doc['id'])

                result.append(doc)

            sorted_data = sorted(result, key=lambda x: x["doc_ordinal"])
            return Response(sorted_data, status=status.HTTP_200_OK)
        else:
            response_msg = {
                "error_code": status.HTTP_400_BAD_REQUEST,
                "description": "Thiếu thông tin hồ sơ"
            }
            return Response(response_msg, status=status.HTTP_200_OK)


class DeleteDocumentById(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongo_client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        self.mongo_collection = self.mongo_client[settings.MONGO_DB_NAME][settings.MONGO_FTS_COLLECTION_NAME]

    def delete_fts_db(self, document_id):
        self.mongo_collection.delete_many({"doc_id": int(document_id)})
        self.mongo_collection.delete_many({"doc_id": str(document_id)})
        return 0

    def post(self, request):
        document_id = request.data.get('id')
        document = get_object_or_404(Document, id=document_id)
        document.delete()
        self.delete_fts_db(document_id)
        return Response(status=status.HTTP_200_OK)


class UpdateDocumentById(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        document_id = request.data.get('id')
        document = get_object_or_404(Document, id=document_id)

        serializer = DocumentSerializer(instance=document, data=dict(request.data.items()), partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            response_msg = {
                "error_code": status.HTTP_400_BAD_REQUEST,
                "description": "Invalid data"
            }
            return Response(response_msg, status=status.HTTP_200_OK)


class DisplayPdfView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request, gov_file_id, doc_id):
        doc_instance = get_object_or_404(Document, id=doc_id)

        file_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT,
                                 settings.DOCUMENT_PATH, str(gov_file_id), doc_instance.doc_name)

        with open(file_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=' + doc_instance.doc_name
            return response


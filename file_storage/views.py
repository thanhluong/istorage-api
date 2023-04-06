from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import Document, GovFile
from .serializers import DocumentUploadSerializer, GovFileSerializer

import os


class GetFiles(APIView):
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        docs = GovFile.objects.all()
        serializer = GovFileSerializer(docs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

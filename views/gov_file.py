from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# from django.conf import settings
# from django.shortcuts import get_object_or_404

from file_storage.models import GovFile
from file_storage.serializers import GovFileSerializer

# import os


class GetFiles(APIView):
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        docs = GovFile.objects.all()
        serializer = GovFileSerializer(docs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

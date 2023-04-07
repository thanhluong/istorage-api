from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404

from file_storage.models import GovFile
from file_storage.serializers import GovFileSerializer


class GetGovFiles(APIView):
    def get(self, request, *args, **kwargs):
        # gov_file_id = request.query_params.get('gov_file_id')
        #
        # if gov_file_id:
        #     try:
        #         gov_file = GovFile.objects.get(gov_file_id=gov_file_id)
        #         serializer = GovFileSerializer(gov_file)
        #         return Response(serializer.data, status=status.HTTP_200_OK)
        #     except GovFile.DoesNotExist:
        #         return Response({"detail": "File not found."}, status=status.HTTP_404_NOT_FOUND)
        # else:
        #     files = GovFile.objects.all()
        #     serializer = GovFileSerializer(files, many=True)
        #     return Response(serializer.data, status=status.HTTP_200_OK)

        files = GovFile.objects.all()
        serializer = GovFileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateGovFile(APIView):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = GovFileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteGovFileById(APIView):
    def delete(self, request, gov_file_id):
        gov_file = get_object_or_404(GovFile, id=gov_file_id)
        gov_file.delete()
        return Response(status=status.HTTP_200_OK)


class UpdateGovFileById(APIView):
    def patch(self, request, gov_file_id):
        gov_file = get_object_or_404(GovFile, id=gov_file_id)
        serializer = GovFileSerializer(instance=gov_file, data=dict(request.data.items()), partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

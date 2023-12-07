from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from file_storage.serializers import OrganSerializer
from file_storage.models import Organ


class OrganListApiView(APIView):
    # 1. List all
    def get(self, request, *args, **kwargs):
        organs = Organ.objects.all()
        serializer = OrganSerializer(organs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 3. Create
    def post(self, request, *args, **kwargs):
        serializer = OrganSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganDetailApiView(APIView):
    def get_object(self, organ_id, *args, **kwargs):
        try:
            return Organ.objects.get(id=organ_id)
        except Organ.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, organ_id, *args, **kwargs):
        organ_instance = self.get_object(organ_id)
        if organ_instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrganSerializer(organ_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, organ_id, *args, **kwargs):
        organ_instance = self.get_object(organ_id)
        if organ_instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrganSerializer(organ_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, organ_id, *args, **kwargs):
        organ_instance = self.get_object(organ_id)
        if organ_instance is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        organ_instance.delete()
        return Response(status=status.HTTP_200_OK)

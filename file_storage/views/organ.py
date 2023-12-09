from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from file_storage.serializers import OrganSerializer
from file_storage.serializers import OrganDepartmentSerializer
from file_storage.models import Organ
from file_storage.models import OrganDepartment


class OrganListApiView(APIView):
    permission_classes = (permissions.AllowAny,)

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
    permission_classes = (permissions.AllowAny,)

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


class OrganDepartmentListApiView(APIView):
    permission_classes = (permissions.AllowAny,)

    # 1. List all
    def get(self, request, *args, **kwargs):
        organDepartments = OrganDepartment.objects.all()
        serializer = OrganDepartmentSerializer(organDepartments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 3. Create
    def post(self, request, *args, **kwargs):
        serializer = OrganDepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganDepartmentDetailApiView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_object(self, organ_department_id, *args, **kwargs):
        try:
            return OrganDepartment.objects.get(id=organ_department_id)
        except OrganDepartment.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, organ_department_id, *args, **kwargs):
        organ_department_instance = self.get_object(organ_department_id)
        if organ_department_instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrganDepartmentSerializer(organ_department_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, organ_department_id, *args, **kwargs):
        organ_department_instance = self.get_object(organ_department_id)
        if organ_department_instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrganDepartmentSerializer(organ_department_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, organ_department_id, *args, **kwargs):
        organ_department_instance = self.get_object(organ_department_id)
        if organ_department_instance is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        organ_department_instance.delete()
        return Response(status=status.HTTP_200_OK)


class OrganDepartmentByOrganIdListView(APIView):
    permission_classes = (permissions.AllowAny,)

    # 1. List all
    def get(self, request, organ_id, *args, **kwargs):
        organDepartments = OrganDepartment.objects.filter(organ_id=organ_id)
        serializer = OrganDepartmentSerializer(organDepartments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
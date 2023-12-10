from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication

from file_storage.serializers import StorageDurationSerializer
from file_storage.serializers import PhysicalStateSerializer
from file_storage.serializers import GovFileLanguageSerializer
from file_storage.serializers import CategoryFileSerializer

from file_storage.models import StorageDuration
from file_storage.models import PhysicalState
from file_storage.models import GovFileLanguage
from file_storage.models import CategoryFile


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class StorageDurationListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        storage_durations = StorageDuration.objects.all()
        serializer = StorageDurationSerializer(storage_durations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StorageDurationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StorageDurationDetailView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get_object(self, storage_duration_id, *args, **kwargs):
        try:
            return StorageDuration.objects.get(id=storage_duration_id)
        except StorageDuration.DoesNotExist:
            return None

    def get(self, request, storage_duration_id):
        storage_duration = self.get_object(storage_duration_id)
        if storage_duration is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StorageDurationSerializer(storage_duration)
        return Response(serializer.data)

    def put(self, request, storage_duration_id):
        storage_duration = self.get_object(storage_duration_id)
        if storage_duration is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StorageDurationSerializer(storage_duration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, storage_duration_id):
        storage_duration = self.get_object(storage_duration_id)
        if storage_duration is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        storage_duration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PhysicalStateListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        physical_states = PhysicalState.objects.all()
        serializer = PhysicalStateSerializer(physical_states, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PhysicalStateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhysicalStateDetailView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get_object(self, physical_state_id, *args, **kwargs):
        try:
            return PhysicalState.objects.get(id=physical_state_id)
        except PhysicalState.DoesNotExist:
            return None

    def get(self, request, physical_state_id):
        physical_state = self.get_object(physical_state_id)
        if physical_state is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PhysicalStateSerializer(physical_state)
        return Response(serializer.data)

    def put(self, request, physical_state_id):
        physical_state = self.get_object(physical_state_id)
        if physical_state is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PhysicalStateSerializer(physical_state, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, physical_state_id):
        physical_state = self.get_object(physical_state_id)
        if physical_state is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        physical_state.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
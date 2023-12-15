from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication

from file_storage.serializers import WarehouseSerializer
from file_storage.serializers import WarehouseRoomSerializer
from file_storage.serializers import ShelfSerializer
from file_storage.serializers import DrawerSerializer

from file_storage.models import Warehouse
from file_storage.models import WarehouseRoom
from file_storage.models import Shelf
from file_storage.models import Drawer
from file_storage.models import GovFile


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class WarehouseListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        warehouse = Warehouse.objects.all()
        serializer = WarehouseSerializer(warehouse, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WarehouseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WarehouseDetailView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, warehouse_id, *args, **kwargs):
        try:
            return Warehouse.objects.get(id=warehouse_id)
        except Warehouse.DoesNotExist:
            return None

    def get(self, request, warehouse_id):
        warehouse = self.get_object(warehouse_id)
        if warehouse is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WarehouseSerializer(warehouse)
        return Response(serializer.data)

    def put(self, request, warehouse_id):
        warehouse = self.get_object(warehouse_id)
        if warehouse is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WarehouseSerializer(warehouse, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WarehouseByOrganIdListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, organ_id, *args, **kwargs):
        try:
            return Warehouse.objects.filter(organ=organ_id)
        except Warehouse.DoesNotExist:
            return None

    def get(self, request, organ_id):
        warehouse = self.get_object(organ_id)
        if warehouse is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WarehouseSerializer(warehouse, many=True)
        return Response(serializer.data)


class WarehouseRoomListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        warehouse_room = WarehouseRoom.objects.all()
        serializer = WarehouseRoomSerializer(warehouse_room, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WarehouseRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WarehouseRoomDetailView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, warehouse_room_id, *args, **kwargs):
        try:
            return WarehouseRoom.objects.get(id=warehouse_room_id)
        except WarehouseRoom.DoesNotExist:
            return None

    def get(self, request, warehouse_room_id):
        warehouse_room = self.get_object(warehouse_room_id)
        if warehouse_room is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WarehouseRoomSerializer(warehouse_room)
        return Response(serializer.data)

    def put(self, request, warehouse_room_id):
        warehouse_room = self.get_object(warehouse_room_id)
        if warehouse_room is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WarehouseRoomSerializer(warehouse_room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, warehouse_room_id):
        warehouse_room = self.get_object(warehouse_room_id)
        if warehouse_room is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        warehouse_room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WarehouseRoomByWarehouseIdListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, warehouse_id, *args, **kwargs):
        try:
            return WarehouseRoom.objects.filter(warehouse=warehouse_id)
        except WarehouseRoom.DoesNotExist:
            return None

    def get(self, request, warehouse_id):
        warehouse_room = self.get_object(warehouse_id)
        if warehouse_room is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WarehouseRoomSerializer(warehouse_room, many=True)
        return Response(serializer.data)


class ShelfListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        shelf = Shelf.objects.all()
        serializer = ShelfSerializer(shelf, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShelfSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShelfDetailView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, shelf_id, *args, **kwargs):
        try:
            return Shelf.objects.get(id=shelf_id)
        except Shelf.DoesNotExist:
            return None

    def get(self, request, shelf_id):
        shelf = self.get_object(shelf_id)
        if shelf is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ShelfSerializer(shelf)
        return Response(serializer.data)

    def put(self, request, shelf_id):
        shelf = self.get_object(shelf_id)
        if shelf is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ShelfSerializer(shelf, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, shelf_id):
        shelf = self.get_object(shelf_id)
        if shelf is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        shelf.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShelfByWarehouseRoomIdListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, warehouse_room_id, *args, **kwargs):
        try:
            return Shelf.objects.filter(warehouse_room=warehouse_room_id)
        except Shelf.DoesNotExist:
            return None

    def get(self, request, warehouse_room_id):
        shelf = self.get_object(warehouse_room_id)
        if shelf is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ShelfSerializer(shelf, many=True)
        return Response(serializer.data)


class DrawerListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        drawer = Drawer.objects.all()
        serializer = DrawerSerializer(drawer, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DrawerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DrawerDetailView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, drawer_id, *args, **kwargs):
        try:
            return Drawer.objects.get(id=drawer_id)
        except Drawer.DoesNotExist:
            return None

    def get(self, request, drawer_id):
        drawer = self.get_object(drawer_id)
        if drawer is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DrawerSerializer(drawer)
        return Response(serializer.data)

    def put(self, request, drawer_id):
        drawer = self.get_object(drawer_id)
        if drawer is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DrawerSerializer(drawer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, drawer_id):
        drawer = self.get_object(drawer_id)
        if drawer is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        drawer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DrawerByShelfIdListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, shelf_id, *args, **kwargs):
        try:
            return Drawer.objects.filter(shelf=shelf_id)
        except Drawer.DoesNotExist:
            return None

    def get(self, request, shelf_id):
        drawer = self.get_object(shelf_id)
        if drawer is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DrawerSerializer(drawer, many=True)
        return Response(serializer.data)


class DrawerAssignmentView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        drawer_id = request.data[0]['drawer_id']
        gov_file_id = request.data[0]['gov_file_id']
        if drawer_id and gov_file_id:
            gov_file = GovFile.objects.get(id=gov_file_id)
            drawer = Drawer.objects.get(id=drawer_id)
            gov_file.drawer = drawer
            gov_file.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
from django.contrib.auth import login, logout
from braces.views import CsrfExemptMixin

from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from file_storage.models import StorageUser
from file_storage.serializers import StorageUserSerializer, StorageUserCreationSerializer


class StorageUserListApiView(CsrfExemptMixin, APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # 1. List all
    def get(self, request, *args, **kwargs):
        users = StorageUser.objects.all()
        serializer = StorageUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 3. Create
    def post(self, request, *args, **kwargs):
        serializer = StorageUserCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StorageUserDetailApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get_object(self, user_id, *args, **kwargs):
        try:
            return StorageUser.objects.get(id=user_id)
        except StorageUser.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, user_id, *args, **kwargs):
        user_instance = self.get_object(user_id)
        if user_instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StorageUserSerializer(user_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, user_id, *args, **kwargs):
        user_instance = self.get_object(user_id)
        if user_instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StorageUserSerializer(user_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, user_id, *args, **kwargs):
        user_instance = self.get_object(user_id)
        if user_instance is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_instance.delete()
        return Response(status=status.HTTP_200_OK)


class StorageUserByDepartmentListView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, department_id, *args, **kwargs):
        users = StorageUser.objects.filter(department_id=department_id)
        serializer = StorageUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StorageUserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = StorageUser.objects.filter(email=email).first()
        if user is None:
            return Response(data={"message": "Không tồn tại người dùng"}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response(data={"message": "Sai tên đăng nhập hoặc mật khẩu"}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        serializer = StorageUserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class StorageUserLogoutView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class StorageUserInfoView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        serializer = StorageUserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class StorageUserSetPasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get_object(self, user_id, *args, **kwargs):
        try:
            return StorageUser.objects.get(id=user_id)
        except StorageUser.DoesNotExist:
            return None

    def post(self, request, user_id, *args, **kwargs):
        user = self.get_object(user_id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        new_password = request.data.get('new_password')
        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)
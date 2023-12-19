import requests

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

EOFFICE_HOST = 'https://office.quangngai.gov.vn/qlvb_qni'

class EofficeLoginView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, username, password):
        login_url = EOFFICE_HOST + '/api/login/v3/'
        res = requests.post(login_url, json={'username': username, 'password': password})
        return Response({"token": res.headers["X-AUTHENTICATION-TOKEN"]}, status=status.HTTP_200_OK)
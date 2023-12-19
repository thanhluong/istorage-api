import requests

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

EOFFICE_HOST = 'https://office.quangngai.gov.vn/qlvb_qni'


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class EofficeLoginView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    def get(self, request, username, password):
        login_url = EOFFICE_HOST + '/api/login/v3/'
        res = requests.post(login_url, json={'username': username, 'password': password})
        return Response({"token": res.headers["X-AUTHENTICATION-TOKEN"]}, status=status.HTTP_200_OK)


class EofficeDocumentListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        url = EOFFICE_HOST + '/api/document/getlistlookupbyparam/'
        res = requests.post(
            url,
            json=request.data,
            headers={'X-AUTHENTICATION-TOKEN': request.headers["X-AUTHENTICATION-TOKEN"]}
        )
        return Response(res.json(), status=res.status_code)
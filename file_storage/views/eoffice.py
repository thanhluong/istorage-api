import requests
import base64

from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

EOFFICE_HOST = 'https://office.quangngai.gov.vn/qlvb_qni'


def decode_base64(data):
    data_bytes = data.encode('ascii')
    decoded_bytes = base64.b64decode(data_bytes)
    return decoded_bytes


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
        return Response(res.json(), status=status.HTTP_200_OK)


class EofficeAttachmentListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request, document_id):
        url = EOFFICE_HOST + '/api/file/getfileattach/' + document_id + '/'
        res = requests.get(
            url,
            headers={'X-AUTHENTICATION-TOKEN': request.headers["X-AUTHENTICATION-TOKEN"]}
        )
        return Response(res.json(), status=status.HTTP_200_OK)


class EofficeAttachmentDownloadView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request, attachment_id):
        url = EOFFICE_HOST + '/api/file/downloaddocument/' + attachment_id + '/'
        res = requests.get(
            url,
            headers={'X-AUTHENTICATION-TOKEN': request.headers["X-AUTHENTICATION-TOKEN"]}
        )
        response = HttpResponse(decode_base64(res.json()["data"]["data"]), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=attachment.pdf'
        return response

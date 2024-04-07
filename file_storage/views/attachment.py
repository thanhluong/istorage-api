from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from django.conf import settings
import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

class DownloadAttachment(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request, dir, file_name):
        file_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'plan', dir, file_name)

        with open(file_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=' + file_name
            return response

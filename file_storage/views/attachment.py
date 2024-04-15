from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from django.conf import settings
import os
from django.http import HttpResponse
from file_storage.models import Attachment, Plan
from file_storage.serializers import AttachmentSerializer
from rest_framework.response import Response


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class DownloadAttachment(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request, dir, file_name):
        file_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'plan', dir, file_name)

        with open(file_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=' + file_name
            return response


class GetAttachmentsByPlanId(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request, plan_id):
        attachments = Attachment.objects.filter(plan_id=plan_id)
        serializer = AttachmentSerializer(attachments, many=True)
        for i in range(len(serializer.data)):
            serializer.data[i]['name'] = serializer.data[i]['file'].split('/')[-1]
            serializer.data[i]['url'] = serializer.data[i]['file'].split('/api/media/')[-1]
        return Response(serializer.data, status=status.HTTP_200_OK)


class AttachmentAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def add_new_file(self, plan_id, request):
        idx = 0
        plan = Plan.objects.get(id=plan_id)
        while f'attachment{idx}' in request.data:
            serializer = AttachmentSerializer(data={
                "file": request.data[f'attachment{idx}'],
                "plan": plan.pk,
            })
            if serializer.is_valid():
                serializer.save()
            else:
                return False
            idx += 1
        return True

    def post(self, request, plan_id):
        success = self.add_new_file(plan_id, request)
        if not success:
            return Response(data={"message": "Failed to add attachment"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)

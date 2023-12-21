from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.renderers import JSONRenderer

from unidecode import unidecode
from datetime import datetime
import json

from file_storage.models import GovFile, GovFileProfile
from file_storage.serializers import GovFileSerializer, GovFileProfileSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


def convert_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")



class KhaithacGovFileListView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def filter_by_fields(self, field, filter_field):
        if filter_field and field != filter_field:
            return False
        return True

    def format_string(self, text):
        words = text.split()
        trimmed_text = " ".join(words)
        format_text = unidecode(trimmed_text.lower())
        return format_text

    def check_title(self, title, search):
        title = self.format_string(title)
        search = self.format_string(search)

        search_idx = title.find(search)
        if search_idx == -1:
            return False
        if search_idx > 0 and title[search_idx - 1] != ' ':
            return False
        if search_idx + len(search) < len(title) and title[search_idx + len(search)] != ' ':
            return False

        return True

    def get(self, request, *args, **kwargs):
        filter_id = int(request.GET.get('id')) if 'id' in request.GET else None
        filter_state = str(request.GET.get('state')) if 'state' in request.GET else None
        filter_start_date = convert_date(request.GET.get('start_date')) if 'start_date' in request.GET else None
        filter_end_date = convert_date(request.GET.get('end_date')) if 'end_date' in request.GET else None
        filter_title = request.GET.get('title') if 'title' in request.GET else None
        filter_plannlls = request.GET.get('plannlls') if 'plannlls' in request.GET else None
        filter_plantieuhuy = request.GET.get('plantieuhuy') if 'plantieuhuy' in request.GET else None

        files = GovFile.objects.all()

        if filter_plannlls:
            files = files.filter(plan_nopluuls__id=filter_plannlls)
        if filter_plantieuhuy:
            files = files.filter(plan_tieuhuy__id=filter_plantieuhuy)

        serializer = GovFileSerializer(files, many=True)
        response_data = []

        for file_info_od in serializer.data:
            file_info_dic = dict(file_info_od)
            gov_file_id = file_info_dic['id']

            profile = GovFileProfile.objects.filter(gov_file_id=gov_file_id).first()
            profile_serialized = GovFileProfileSerializer(profile)

            profile_data = json.loads(JSONRenderer().render(profile_serialized.data).decode('utf-8'))
            if not profile_data or not profile_data['state']:
                continue

            id = file_info_od['id']
            state = str(profile_data['state'])
            start_date = convert_date(file_info_od['start_date']) if file_info_od['start_date'] else None
            end_date = convert_date(file_info_od['end_date']) if file_info_od['end_date'] else None
            title = file_info_od['title'] if 'title' in file_info_od else None

            filter_fields = ['id', 'state', 'start_date', 'end_date']
            is_selected = True
            for field in filter_fields:
                check_str = "self.filter_by_fields(" + field + ", filter_" + field + ")"
                if not eval(check_str):
                    is_selected = False
                    break
            if not is_selected:
                continue

            if filter_title:
                if not title:
                    continue
                if not self.check_title(title, filter_title):
                    continue

            file_info_dic['state'] = state
            response_data.append(file_info_dic)

        return Response(response_data, status=status.HTTP_200_OK)


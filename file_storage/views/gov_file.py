from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import SessionAuthentication
from django.shortcuts import get_object_or_404
from django.conf import settings

from file_storage.models import GovFile, GovFileProfile
from file_storage.serializers import GovFileSerializer, GovFileProfileSerializer

import json
from datetime import datetime
from unidecode import unidecode
from enum import Enum
from pymongo import MongoClient


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


def convert_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")


NHAP_LIEU = 1
DUYET_CO_QUAN = 2
DUYET_LICH_SU = 3
ADMIN = 4

STT_MO = 1
STT_DONG = 2
STT_NOP_LUU_CQ = 3
STT_LUU_TRU_CQ = 4
STT_NOP_LUU_LS = 5
STT_LUU_TRU_LS = 6
STT_TRA_VE = 7
STT_TRA_VE_LS = 8
STT_DA_NHAN_NOP_LUU = 9
STT_CHO_XEP_KHO = 10
STT_HSCL_TAO_MOI = 11
STT_HSCL_GIAO_NOP = 12
STT_HSCL_BI_TRA_VE = 13

perm_read_dict = {
    NHAP_LIEU: [STT_MO, STT_DONG, STT_NOP_LUU_CQ],
    DUYET_CO_QUAN: [STT_NOP_LUU_CQ, STT_LUU_TRU_CQ, STT_NOP_LUU_LS],
    DUYET_LICH_SU: [STT_NOP_LUU_LS, STT_LUU_TRU_LS],
    ADMIN: [STT_MO, STT_DONG, STT_NOP_LUU_CQ, STT_LUU_TRU_CQ, STT_NOP_LUU_LS, STT_LUU_TRU_LS]
}


class GetGovFiles(APIView):
    permission_classes = (permissions.IsAuthenticated,)
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

        files = None
        if request.user.is_authenticated:
            if request.user.is_superuser:
                files = GovFile.objects.all()
            else:
                organ_id = 0
                if request.user.department and request.user.department.organ:
                    organ_id = request.user.department.organ.id
                files = GovFile.objects.filter(identifier__id=organ_id)

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


class CreateGovFile(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        # date_error_msg = {
        #     "error_code": status.HTTP_400_BAD_REQUEST,
        #     "description": "Ngày bắt đầu hoặc kết thúc không hợp lệ"
        # }
        # resp_date_error = Response(date_error_msg, status=status.HTTP_200_OK)
        #
        # if "start_date" not in request.data:
        #     return resp_date_error
        # try:
        #     start_date = convert_date(request.data.get('start_date'))
        #     if "end_date" in request.data and request.data.get('end_date'):
        #         end_date = convert_date(request.data.get('end_date'))
        #
        #         if start_date > end_date:
        #             return resp_date_error
        # except ValueError:
        #     return resp_date_error

        serializer = GovFileSerializer(data=request.data)
        print(serializer)

        if serializer.is_valid():
            serializer.save()

            gov_file_profile = {
                "gov_file_id": serializer.data['id'],
                "state": STT_MO
            }
            profile_serializer = GovFileProfileSerializer(data=gov_file_profile)
            if profile_serializer.is_valid():
                profile_serializer.save()
            else:
                response_msg = {
                    "error_code": status.HTTP_400_BAD_REQUEST,
                    "description": "Request data not valid"
                }
                Response(response_msg, status=status.HTTP_200_OK)

            response_data = serializer.data
            response_data['state'] = STT_MO
            return Response(response_data, status=status.HTTP_201_CREATED)

        response_msg = {
            "error_code": status.HTTP_400_BAD_REQUEST,
            "description": serializer.errors
        }
        return Response(response_msg, status=status.HTTP_200_OK)


class DeleteGovFileById(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongo_client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        self.mongo_collection = self.mongo_client[settings.MONGO_DB_NAME][settings.MONGO_FTS_COLLECTION_NAME]

    def delete_fts_db(self, gov_file_id):
        self.mongo_collection.delete_many({"gov_file_id": int(gov_file_id)})
        self.mongo_collection.delete_many({"gov_file_id": str(gov_file_id)})
        return 0

    def post(self, request):
        gov_file_id = request.data.get('id')
        print(type(gov_file_id))

        perm_response_msg = {
            "error_code": status.HTTP_401_UNAUTHORIZED,
            "description": "Bạn không có quyền xóa hồ sơ này!",

        }

        gov_file = GovFile.objects.filter(id=gov_file_id)
        gov_file_profile = GovFileProfile.objects.filter(gov_file_id=gov_file_id).first()
        profile_serializer = GovFileProfileSerializer(gov_file_profile)
        profile_json = json.loads(JSONRenderer().render(profile_serializer.data).decode('utf-8'))
        if not gov_file:
            response_msg = {
                "error_code": status.HTTP_404_NOT_FOUND,
                "description": "Hồ sơ không tồn tại!",

            }
            return Response(response_msg, status=status.HTTP_200_OK)

        gov_file.delete()
        gov_file_profile.delete()
        self.delete_fts_db(gov_file_id)
        response_msg = {
            "description": "Đã xóa hồ sơ thành công!",

        }
        return Response(response_msg, status=status.HTTP_200_OK)


class UpdateGovFileById(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        gov_file_id = request.data.get('id')
        gov_file = GovFile.objects.filter(id=gov_file_id)

        if not request.user.is_superuser:
            if not request.user.department or not request.user.department.organ:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            organ_id = request.user.department.organ.id
            gov_organ_id = gov_file.first().identifier.id

            if organ_id != gov_organ_id:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        if gov_file:
            gov_file = gov_file.first()
            gov_file_serialized = GovFileSerializer(gov_file)
            gov_file_data = json.loads(JSONRenderer().render(gov_file_serialized.data).decode('utf-8'))

            try:
                start_date = convert_date(request.data.get('start_date')) \
                    if "start_date" in request.data else convert_date(gov_file_data.get('start_date'))
            except ValueError:
                response_msg = {
                    "error_code": status.HTTP_400_BAD_REQUEST,
                    "description": "Ngày bắt đầu không hợp lệ!"
                }
                return Response(response_msg, status=status.HTTP_200_OK)

            if "end_date" in request.data and request.data.get('end_date'):
                date_error_msg = {
                    "error_code": status.HTTP_400_BAD_REQUEST,
                    "description": "Ngày bắt đầu hoặc kết thúc không hợp lệ!"
                }
                try:
                    end_date = convert_date(request.data.get('end_date'))
                    if end_date < start_date:
                        return Response(date_error_msg, status=status.HTTP_200_OK)
                except ValueError:
                    return Response(date_error_msg, status=status.HTTP_200_OK)

            serializer = GovFileSerializer(instance=gov_file, data=dict(request.data.items()), partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                response_msg = {
                    "error_code": status.HTTP_400_BAD_REQUEST,
                    "description": serializer.errors
                }
                return Response(response_msg, status=status.HTTP_200_OK)

        else:
            response_msg = {
                "error_code": status.HTTP_404_NOT_FOUND,
                "description": "Không tìm thấy hồ sơ"
            }
            return Response(response_msg, status=status.HTTP_200_OK)


class UpdateGovFileStateById(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        """
            1: mo, 2: dong, 3: nop luu co quan, 4: luu tru co quan, 5: nop luu lich su, 6: luu tru lich su
            7: tra ve, 8: tra ve lich su
        """
        # state_machine = {
        #     STT_MO: [STT_DONG],
        #     STT_DONG: [STT_MO, STT_NOP_LUU_CQ],
        #     STT_NOP_LUU_CQ: [STT_TRA_VE, STT_LUU_TRU_CQ],
        #     STT_LUU_TRU_CQ: [STT_TRA_VE, STT_NOP_LUU_CQ, STT_NOP_LUU_LS],
        #     STT_NOP_LUU_LS: [STT_TRA_VE_LS, STT_LUU_TRU_CQ, STT_LUU_TRU_LS],
        #     STT_LUU_TRU_LS: [STT_TRA_VE_LS, STT_LUU_TRU_CQ],
        #     STT_TRA_VE: [STT_MO, STT_NOP_LUU_CQ, STT_LUU_TRU_CQ],
        #     STT_TRA_VE_LS: [STT_MO, STT_NOP_LUU_CQ, STT_LUU_TRU_CQ, STT_NOP_LUU_LS, STT_LUU_TRU_LS],
        #     STT_DA_NHAN_NOP_LUU: [STT_CHO_XEP_KHO],
        #     STT_CHO_XEP_KHO: [STT_LUU_TRU_CQ],
        #     STT_HSCL_TAO_MOI: [STT_HSCL_GIAO_NOP],
        #     STT_HSCL_GIAO_NOP: [STT_HSCL_BI_TRA_VE, STT_CHO_XEP_KHO],
        #     STT_HSCL_BI_TRA_VE: [STT_HSCL_GIAO_NOP]
        # }

        response_data = []
        serializer_list = []
        if not isinstance(request.data, list):
            response_msg = {
                "error_code": status.HTTP_400_BAD_REQUEST,
                "description": "Request body must list of json object"
            }
            return Response(response_msg, status=status.HTTP_200_OK)

        for json_data in request.data:
            gov_file_id = str(json_data['id'])

            gov_file = GovFile.objects.filter(id=gov_file_id).first()
            profile = GovFileProfile.objects.filter(gov_file_id=gov_file_id).first()

            if not gov_file or not profile:
                response_msg = {
                    'error_code': status.HTTP_404_NOT_FOUND,
                    'description': 'Không tìm thấy hồ sơ'
                }
                return Response(response_msg, status=status.HTTP_200_OK)

            gov_file_serialized = GovFileSerializer(gov_file)
            gov_file_data = json.loads(JSONRenderer().render(gov_file_serialized.data).decode('utf-8'))

            profile_serialized = GovFileProfileSerializer(profile)
            profile_data = json.loads(JSONRenderer().render(profile_serialized.data).decode('utf-8'))

            # Check if profile_data exists
            if not profile_data or not profile_data['state']:
                response_msg = {
                    "error_code": status.HTTP_404_NOT_FOUND,
                    "description": "Không có trạng thái nào cho hồ sơ với id " + gov_file_id
                }
                return Response(response_msg, status=status.HTTP_200_OK)

            current_state = int(profile_data['state'])

            # Check if the transfer state process is valid
            new_state = int(json_data['new_state'])
            # if new_state not in state_machine[current_state]:
            #     response_msg = {
            #         "error_code": status.HTTP_406_NOT_ACCEPTABLE,
            #         "description": "Không cho phép quá trình chuyển trạng thái này của hồ sơ với id " + gov_file_id
            #     }
            #     return Response(response_msg, status=status.HTTP_200_OK)

            # Check when close gov_file, the required fields is not empty
            if current_state == STT_MO and new_state == STT_DONG and not gov_file_data['end_date']:
                response_msg = {
                    'error_code': status.HTTP_400_BAD_REQUEST,
                    'description': "Hồ sơ chưa có ngày kết thúc"
                }
                return Response(response_msg, status=status.HTTP_200_OK)

            new_serializer = GovFileProfileSerializer(profile,
                                                      data={'state': new_state},
                                                      partial=True)

            if new_serializer.is_valid():
                serializer_list.append(new_serializer)

                response_data.append({'id': gov_file_id, 'state': json_data['new_state']})
            else:
                response_msg = {
                    "error_code": status.HTTP_400_BAD_REQUEST,
                    "description": new_serializer.errors
                }
                return Response(response_msg, status=status.HTTP_200_OK)

        for serializer in serializer_list:
            serializer.save()

        return Response(response_data, status=status.HTTP_200_OK)

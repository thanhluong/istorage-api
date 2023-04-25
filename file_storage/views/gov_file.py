from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from braces.views import CsrfExemptMixin

from django.shortcuts import get_object_or_404
from django.conf import settings

from file_storage.models import GovFile, GovFileProfile
from file_storage.serializers import GovFileSerializer, GovFileProfileSerializer

import json
from datetime import datetime
from unidecode import unidecode
from enum import Enum
from pymongo import MongoClient


def convert_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

NHAP_LIEU = 1
DUYET_CO_QUAN = 2
DUYET_LICH_SU = 3
ADMIN = 4

MO = 1
DONG = 2
NOP_LUU_CQ = 3
LUU_TRU_CQ = 4
NOP_LUU_LS = 5
LUU_TRU_LS = 6
TRA_VE = 7
TRA_VE_LS = 8

perm_read_dict = {
    NHAP_LIEU: [MO, DONG, NOP_LUU_CQ],
    DUYET_CO_QUAN: [NOP_LUU_CQ, LUU_TRU_CQ, NOP_LUU_LS],
    DUYET_LICH_SU: [NOP_LUU_LS, LUU_TRU_LS],
    ADMIN: [MO, DONG, NOP_LUU_CQ, LUU_TRU_CQ, NOP_LUU_LS, LUU_TRU_LS]
}


class GetGovFiles(CsrfExemptMixin, APIView):
    authentication_classes = []

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
        if search_idx > 0 and title[search_idx-1] != ' ':
            return False
        if search_idx + len(search) < len(title) and title[search_idx + len(search)] != ' ':
            return False

        return True

    def get(self, request, *args, **kwargs):
        perm_token = int(request.GET.get('perm_token'))

        filter_id = int(request.GET.get('id')) if 'id' in request.GET else None
        filter_state = str(request.GET.get('state')) if 'state' in request.GET else None
        filter_start_date = convert_date(request.GET.get('start_date')) if 'start_date' in request.GET else None
        filter_end_date = convert_date(request.GET.get('end_date')) if 'end_date' in request.GET else None
        filter_title = request.GET.get('title') if 'title' in request.GET else None

        if perm_token not in perm_read_dict:
            response_msg = {
                "error_code": status.HTTP_401_UNAUTHORIZED,
                "description": "Không có quyền!"
            }
            return Response(response_msg, status=status.HTTP_200_OK)

        files = GovFile.objects.all()
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


class CreateGovFile(CsrfExemptMixin, APIView):
    authentication_classes = []
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        date_error_msg = {
            "error_code": status.HTTP_400_BAD_REQUEST,
            "description": "Ngày bắt đầu hoặc kết thúc không hợp lệ"
        }
        resp_date_error = Response(date_error_msg, status=status.HTTP_200_OK)

        if "start_date" not in request.data:
            return resp_date_error
        try:
            start_date = convert_date(request.data.get('start_date'))
            if "end_date" in request.data and request.data.get('end_date'):
                end_date = convert_date(request.data.get('end_date'))

                if start_date > end_date:
                    return resp_date_error
        except ValueError:
            return resp_date_error

        serializer = GovFileSerializer(data=request.data)
        print(serializer)

        if serializer.is_valid():
            serializer.save()

            gov_file_profile = {
                "gov_file_id": serializer.data['id'],
                "state": MO
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
            response_data['state'] = MO
            return Response(response_data, status=status.HTTP_201_CREATED)

        response_msg = {
            "error_code": status.HTTP_400_BAD_REQUEST,
            "description": "Invalid serialize data"
        }
        return Response(response_msg, status=status.HTTP_200_OK)


class DeleteGovFileById(CsrfExemptMixin, APIView):
    authentication_classes = []

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
        # if 'perm_token' in request.data:
        #     perm_token = int(request.data.get('perm_token'))
        # else:
        #     return Response(perm_response_msg, status.HTTP_200_OK)

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

        # if profile_json['state'] and profile_json['state'] not in perm_read_dict[perm_token]:
        #     return Response(perm_response_msg, status.HTTP_200_OK)

        gov_file.delete()
        gov_file_profile.delete()
        self.delete_fts_db(gov_file_id)
        response_msg = {
            "description": "Đã xóa hồ sơ thành công!",

        }
        return Response(response_msg, status=status.HTTP_200_OK)


class UpdateGovFileById(CsrfExemptMixin, APIView):
    authentication_classes = []

    def post(self, request):
        gov_file_id = request.data.get('id')
        gov_file = GovFile.objects.filter(id=gov_file_id)
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
                    "description": "Invalid serialize data"
                }
                return Response(response_msg, status=status.HTTP_200_OK)

        else:
            response_msg = {
                "error_code": status.HTTP_404_NOT_FOUND,
                "description": "Không tìm thấy hồ sơ"
            }
            return Response(response_msg, status=status.HTTP_200_OK)


class UpdateGovFileStateById(CsrfExemptMixin, APIView):
    authentication_classes = []

    def post(self, request):
        """
            1: mo, 2: dong, 3: nop luu co quan, 4: luu tru co quan, 5: nop luu lich su, 6: luu tru lich su
            7: tra ve, 8: tra ve lich su
        """
        state_machine = {
            MO: [DONG],
            DONG: [MO, NOP_LUU_CQ],
            NOP_LUU_CQ: [TRA_VE, LUU_TRU_CQ],
            LUU_TRU_CQ: [TRA_VE, NOP_LUU_CQ, NOP_LUU_LS],
            NOP_LUU_LS: [TRA_VE_LS, LUU_TRU_CQ, LUU_TRU_LS],
            LUU_TRU_LS: [TRA_VE_LS, LUU_TRU_CQ],
            TRA_VE: [NOP_LUU_CQ, LUU_TRU_CQ],
            TRA_VE_LS: [NOP_LUU_LS, LUU_TRU_LS]
        }

        perm_transfer_dict = {
            NHAP_LIEU: [[MO, DONG], [DONG, MO], [DONG, NOP_LUU_CQ]],
            DUYET_CO_QUAN: [[NOP_LUU_CQ, LUU_TRU_CQ], [NOP_LUU_CQ, MO], [LUU_TRU_CQ, MO], [LUU_TRU_CQ, NOP_LUU_LS]],
            DUYET_LICH_SU: [[NOP_LUU_LS, LUU_TRU_LS], [NOP_LUU_LS, LUU_TRU_CQ], [LUU_TRU_LS, LUU_TRU_CQ]],
            ADMIN: [[MO, DONG], [DONG, MO], [DONG, NOP_LUU_CQ],
                    [NOP_LUU_CQ, LUU_TRU_CQ], [NOP_LUU_CQ, MO], [LUU_TRU_CQ, MO], [LUU_TRU_CQ, NOP_LUU_LS],
                    [NOP_LUU_LS, LUU_TRU_LS], [NOP_LUU_LS, LUU_TRU_CQ]],
        }

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

            # Check if request data has permission token
            # if "perm_token" not in json_data:
            #     response_msg = {
            #         "error_code": status.HTTP_401_UNAUTHORIZED,
            #         "description": "Không có quyền với hồ sơ với id " + gov_file_id
            #     }
            #     return Response(response_msg, status=status.HTTP_200_OK)

            # Check if the permission token is valid
            # perm_token = int(json_data["perm_token"])
            # if perm_token not in perm_transfer_dict or \
            #         [json_data["current_state"], json_data["new_state"]] not in perm_transfer_dict[perm_token]:
            #     response_msg = {
            #         "error_code": status.HTTP_401_UNAUTHORIZED,
            #         "description": "Không có quyền với hồ sơ với id " + gov_file_id
            #     }
            #     return Response(response_msg, status=status.HTTP_200_OK)

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
            # Check if the current state of request data exactly
            # if json_data['current_state'] != current_state:
            #    response_msg = {
            #        "error_code": status.HTTP_409_CONFLICT,
            #        "description": "Trạng thái hiện tại không hợp lệ với hồ sơ có id " + gov_file_id
            #    }
            #    return Response(response_msg, status=status.HTTP_200_OK)

            # Check if the transfer state process is valid
            new_state = int(json_data['new_state'])
            if new_state not in state_machine[current_state]:
                response_msg = {
                    "error_code": status.HTTP_406_NOT_ACCEPTABLE,
                    "description": "Không cho phép quá trình chuyển trạng thái này của hồ sơ với id " + gov_file_id
                }
                return Response(response_msg, status=status.HTTP_200_OK)

            # Check when close gov_file, the required fields is not empty
            if current_state == MO and new_state == DONG and not gov_file_data['end_date']:
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
                    "description": "Invalid serialize data"
                }
                return Response(response_msg, status=status.HTTP_200_OK)

        for serializer in serializer_list:
            serializer.save()

        return Response(response_data, status=status.HTTP_200_OK)

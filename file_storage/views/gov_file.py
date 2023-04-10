from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from django.shortcuts import get_object_or_404

from file_storage.models import GovFile, GovFileProfile
from file_storage.serializers import GovFileSerializer, GovFileProfileSerializer

import json
from datetime import datetime


def convert_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")


class GetGovFiles(APIView):
    def filter_by_fields(self, field, filter_field):
        if filter_field and field != filter_field:
            return False
        return True


    def get(self, request, *args, **kwargs):
        perm_read_dict = {
            "1": [1, 2, 3],
            "2": [3, 4, 5],
            "3": [5, 6],
            "4": [1, 2, 3, 4, 5, 6]
        }

        perm_token = request.GET.get('perm_token')
        filter_state = str(request.GET.get('state')) if 'state' in request.GET else None
        filter_start_date = convert_date(request.GET.get('start_date')) if 'start_date' in request.GET else None
        filter_end_date = convert_date(request.GET.get('end_date')) if 'end_date' in request.GET else None
        filter_title = request.GET.get('title') if 'title' in request.GET else None

        if perm_token not in perm_read_dict:
            response_msg = {
                "error_code": status.HTTP_401_UNAUTHORIZED,
                "description": "Unauthorized"
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

            state = str(profile_data['state'])
            start_date = convert_date(file_info_od['start_date']) if 'start_date' in file_info_od else None
            end_date = convert_date(file_info_od['end_date']) if 'end_date' in file_info_od else None
            title = file_info_od['title'] if 'title' in file_info_od else None
            # if state not in perm_read_dict[perm_token] or str(state) != str(filter_state):

            filter_fields = ['state', 'start_date', 'end_date', 'title']
            is_selected = True
            for field in filter_fields:
                check_str = "self.filter_by_fields(" + field + ", filter_" + field + ")"
                if not eval(check_str):
                    is_selected = False
                    break
            if not is_selected:
                continue

            file_info_dic['state'] = state
            response_data.append(file_info_dic)

        return Response(response_data, status=status.HTTP_200_OK)


class CreateGovFile(APIView):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        date_error_msg = {
            "error_code": status.HTTP_400_BAD_REQUEST,
            "description": "Invalid start date or end date"
        }
        resp_date_error = Response(date_error_msg, status=status.HTTP_200_OK)

        if "start_date" not in request.data:
            return resp_date_error
        try:
            start_date = convert_date(request.data.get('start_date'))
            if "end_date" in request.data:
                end_date = convert_date(request.data.get('end_date'))

                if start_date > end_date:
                    return resp_date_error
        except ValueError:
            return resp_date_error

        serializer = GovFileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            gov_file_profile = {
                "gov_file_id": serializer.data['id'],
                "state": 1
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
            response_data['state'] = 1
            return Response(response_data, status=status.HTTP_201_CREATED)

        response_msg = {
            "error_code": status.HTTP_400_BAD_REQUEST,
            "description": "Invalid serialize data"
        }
        return Response(response_msg, status=status.HTTP_200_OK)


class DeleteGovFileById(APIView):
    def delete(self, request):
        gov_file_id = request.GET.get('gov_file_id')
        gov_file = get_object_or_404(GovFile, id=gov_file_id)
        gov_file.delete()
        return Response(status=status.HTTP_200_OK)


class UpdateGovFileById(APIView):
    def patch(self, request):
        gov_file_id = request.GET.get('gov_file_id')
        gov_file = GovFile.objects.filter(id=gov_file_id)
        if gov_file:
            gov_file = gov_file.first()
            gov_file_serialized = GovFileSerializer(gov_file)
            gov_file_data = json.loads(JSONRenderer().render(gov_file_serialized.data).decode('utf-8'))

            try:
                start_date = convert_date(request.data.get('start_date')) \
                    if "start_date" in request.data else gov_file_data.get('start_date')
            except ValueError:
                response_msg = {
                    "error_code": status.HTTP_400_BAD_REQUEST,
                    "description": "Invalid start date"
                }
                return Response(response_msg, status=status.HTTP_200_OK)

            if "end_date" in request.data:
                date_error_msg = {
                    "error_code": status.HTTP_400_BAD_REQUEST,
                    "description": "Invalid start date or end date"
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
                "description": "Gov_file not found"
            }
            return Response(response_msg, status=status.HTTP_200_OK)


class UpdateGovFileStateById(APIView):

    def patch(self, request):
        """
            1: mo, 2: dong, 3: nop luu co quan, 4: luu tru co quan, 5: nop luu lich su, 6: luu tru lich su
        """
        state_machine = {
            "1": [2],
            "2": [1, 3],
            "3": [1, 4],
            "4": [2, 5],
            "5": [4, 6],
            "6": [4]
        }

        perm_transfer_dict = {
            "1": [[1, 2], [2, 1], [2, 3]],
            "2": [[3, 4], [3, 1], [4, 5]],
            "3": [[5, 6], [5, 4]],
            "4": [[1, 2], [2, 1], [2, 3], [3, 4], [3, 1], [4, 5], [5, 6], [5, 4]],
        }

        response_data = []
        serializer_list = []
        if isinstance(request.data, list):
            for json_data in request.data:
                gov_file_id = str(json_data['gov_file_id'])

                # Check if request data has permission token
                if "perm_token" not in json_data:
                    response_msg = {
                        "error_code": status.HTTP_401_UNAUTHORIZED,
                        "description": "Don't have permission for file with id " + gov_file_id
                    }
                    return Response(response_msg, status=status.HTTP_200_OK)

                # Check if the permission token is valid
                perm_token = str(json_data["perm_token"])
                if perm_token not in perm_transfer_dict or \
                        [json_data["current_state"], json_data["new_state"]] not in perm_transfer_dict[perm_token]:
                    response_msg = {
                        "error_code": status.HTTP_401_UNAUTHORIZED,
                        "description": "Don't have permission for file with id " + gov_file_id
                    }
                    return Response(response_msg, status=status.HTTP_200_OK)

                gov_file = GovFile.objects.filter(id=gov_file_id)
                profile = GovFileProfile.objects.filter(gov_file_id=gov_file_id)
                if not gov_file or not profile:
                    response_msg = {
                        'error_code': status.HTTP_404_NOT_FOUND,
                        'description': 'Gov_file not found'
                    }
                    return Response(response_msg, status=status.HTTP_200_OK)

                gov_file_serialized = GovFileSerializer(gov_file.first())
                gov_file_data = json.loads(JSONRenderer().render(gov_file_serialized.data).decode('utf-8'))

                profile_serialized = GovFileProfileSerializer(profile.first())
                profile_data = json.loads(JSONRenderer().render(profile_serialized.data).decode('utf-8'))

                # Check if profile_data exists
                if not profile_data or not profile_data['state']:
                    response_msg = {
                        "error_code": status.HTTP_404_NOT_FOUND,
                        "description": "Don't have any state for the gov_file correspond to id " + gov_file_id
                    }
                    return Response(response_msg, status=status.HTTP_200_OK)

                current_state = profile_data['state']
                # Check if the current state of request data exactly
                if json_data['current_state'] != current_state:
                    response_msg = {
                        "error_code": status.HTTP_409_CONFLICT,
                        "description": "Conflict in current state for file with id " + gov_file_id
                    }
                    return Response(response_msg, status=status.HTTP_200_OK)

                # Check if the transfer state process is valid
                new_state = json_data['new_state']
                if new_state not in state_machine[str(current_state)]:
                    response_msg = {
                        "error_code": status.HTTP_406_NOT_ACCEPTABLE,
                        "description": "Not allow for that transfer state for file with id " + gov_file_id
                    }
                    return Response(response_msg, status=status.HTTP_200_OK)

                # Check when close gov_file, the required fields is not empty
                if current_state == 1 and new_state == 2 and 'end_date' not in gov_file_data:
                    response_msg = {
                        'error_code': status.HTTP_400_BAD_REQUEST,
                        'description': "Gov_file doesn't have end date"
                    }
                    return Response(response_msg, status=status.HTTP_200_OK)

                new_serializer = GovFileProfileSerializer(profile,
                                                          data={'state': json_data['new_state']},
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
        else:
            response_msg = {
                "error_code": status.HTTP_400_BAD_REQUEST,
                "description": "Request body must list of json object"
            }
            return Response(response_msg, status=status.HTTP_200_OK)

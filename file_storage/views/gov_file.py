from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse

from file_storage.models import GovFile, GovFileProfile
from file_storage.serializers import GovFileSerializer, GovFileProfileSerializer

import json


class GetGovFiles(APIView):
    def get(self, request, *args, **kwargs):
        perm_read_dict = {
            "1": [1, 2, 3],
            "2": [3, 4, 5],
            "3": [5, 6],
            "4": [1, 2, 3, 4, 5, 6]
        }

        # request_data = dict(request.data.items())
        # perm_token = str(request_data["perm_token"])
        perm_token = request.GET.get('perm_token')
        if perm_token not in perm_read_dict:
            return Response("Unauthorized!", status=status.HTTP_401_UNAUTHORIZED)

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

            state = profile_data['state']

            if state not in perm_read_dict[perm_token]:
                continue

            file_info_dic['state'] = state
            response_data.append(file_info_dic)

        return Response(response_data, status=status.HTTP_200_OK)


class CreateGovFile(APIView):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
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

            response_data = serializer.data
            response_data['state'] = 1
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteGovFileById(APIView):
    def delete(self, request):
        gov_file_id = request.GET.get('gov_file_id')
        gov_file = get_object_or_404(GovFile, id=gov_file_id)
        gov_file.delete()
        return Response(status=status.HTTP_200_OK)


class UpdateGovFileById(APIView):
    def patch(self, request):
        gov_file_id = request.GET.get('gov_file_id')
        gov_file = get_object_or_404(GovFile, id=gov_file_id)

        serializer = GovFileSerializer(instance=gov_file, data=dict(request.data.items()), partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            for json_object in request.data:
                gov_file_id = str(json_object['gov_file_id'])

                if "perm_token" not in json_object:
                    return Response("Don't have permission for file with id " + gov_file_id,
                                    status=status.HTTP_401_UNAUTHORIZED)
                perm_token = str(json_object["perm_token"])
                if perm_token not in perm_transfer_dict or \
                        [json_object["current_state"], json_object["new_state"]] not in perm_transfer_dict[perm_token]:
                    return Response("Don't have permission for file with id " + gov_file_id,
                                    status=status.HTTP_401_UNAUTHORIZED)

                profile = GovFileProfile.objects.filter(gov_file_id=gov_file_id).first()
                profile_serialized = GovFileProfileSerializer(profile)
                profile_data = json.loads(JSONRenderer().render(profile_serialized.data).decode('utf-8'))
                if not profile_data or not profile_data['state']:
                    return Response("Don't have any state for the gov_file correspond to id " + gov_file_id,
                                    status=status.HTTP_404_NOT_FOUND)

                current_state = profile_data['state']

                if json_object['current_state'] != current_state:
                    return Response('Conflict in current state for file with id ' + gov_file_id,
                                    status=status.HTTP_409_CONFLICT)

                if json_object['new_state'] not in state_machine[str(current_state)]:
                    return Response('Not allow for that transfer state for file with id ' + gov_file_id,
                                    status=status.HTTP_406_NOT_ACCEPTABLE)

                new_serializer = GovFileProfileSerializer(profile, data={'state': json_object['new_state']}, partial=True)
                if new_serializer.is_valid():
                    serializer_list.append(new_serializer)

                    response_data.append({'id': gov_file_id, 'state': json_object['new_state']})
                else:
                    return Response(new_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            for serializer in serializer_list:
                serializer.save()

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response("Request body must list of json object!", status=status.HTTP_400_BAD_REQUEST)



def get_gov_file_pagination(request):
    gov_file_list = GovFile.objects.all()
    page_size = request.GET.get('page_size') # number gov_file per page
    paginator = Paginator(gov_file_list, page_size)  
    page_id = request.GET.get('page_id')
    page_obj = paginator.get_page(page_id)
    serializer = GovFileSerializer(page_obj.object_list, many=True)
    data = {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
        'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'results': serializer.data,
    }
    return JsonResponse(data)
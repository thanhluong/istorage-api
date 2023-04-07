from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from django.shortcuts import get_object_or_404

from file_storage.models import GovFile, GovFileProfile
from file_storage.serializers import GovFileSerializer, GovFileProfileSerializer

import json


class GetGovFiles(APIView):
    def get(self, request, *args, **kwargs):
        # gov_file_id = request.query_params.get('gov_file_id')
        #
        # if gov_file_id:
        #     try:
        #         gov_file = GovFile.objects.get(gov_file_id=gov_file_id)
        #         serializer = GovFileSerializer(gov_file)
        #         return Response(serializer.data, status=status.HTTP_200_OK)
        #     except GovFile.DoesNotExist:
        #         return Response({"detail": "File not found."}, status=status.HTTP_404_NOT_FOUND)
        # else:
        #     files = GovFile.objects.all()
        #     serializer = GovFileSerializer(files, many=True)
        #     return Response(serializer.data, status=status.HTTP_200_OK)

        files = GovFile.objects.all()
        serializer = GovFileSerializer(files, many=True)
        response_data = []

        for file_info_od in serializer.data:
            file_info_dic = dict(file_info_od)
            gov_file_id = file_info_dic['id']
            profile_queryset = GovFileProfile.objects.filter(gov_file_id=gov_file_id)
            profile_serialized = GovFileProfileSerializer(profile_queryset, many=True)

            profile_data_list = json.loads(JSONRenderer().render(profile_serialized.data).decode('utf-8'))
            if not profile_data_list or len(profile_data_list) == 0:
                response_data.append(file_info_dic)
                continue

            file_info_dic['state'] = profile_data_list[0]['state']
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
        gov_file_id = request.GET.get('gov_file_id')
        profile = GovFileProfile.objects.filter(gov_file_id=gov_file_id).first()
        profile_serialized = GovFileProfileSerializer(profile)
        profile_data = json.loads(JSONRenderer().render(profile_serialized.data).decode('utf-8'))
        if not profile_data or not profile_data['state']:
            return Response("Don't have any state for the gov_file correspond to id " + str(gov_file_id),
                            status=status.HTTP_404_NOT_FOUND)

        current_state = profile_data['state']
        data_dict = dict(request.data.items())
        if data_dict['current_state'] != current_state:
            return Response('Conflict in current state!', status=status.HTTP_409_CONFLICT)

        if data_dict['new_state'] not in state_machine[str(current_state)]:
            return Response('Not allow for that transfer state!', status=status.HTTP_406_NOT_ACCEPTABLE)

        new_serializer = GovFileProfileSerializer(profile, data={'state': data_dict['new_state']}, partial=True)
        if new_serializer.is_valid():
            new_serializer.save()
            return Response(new_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(new_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

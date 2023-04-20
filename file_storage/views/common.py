from rest_framework.response import Response
from rest_framework import status


def list_response(given_list):
    result = {
        "error_code": 0,
        "items": given_list
    }
    return Response(result, status=status.HTTP_200_OK)


def error_response(error_code, description):
    result = {
        "error_code": error_code,
        "description": description
    }
    return Response(result, status=status.HTTP_200_OK)
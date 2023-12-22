from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from braces.views import CsrfExemptMixin
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions, status

from django.conf import settings
from .common import *
from pymongo import MongoClient


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


# Error messages
ERR_MESSAGE_NO_KEYWORD = "Bạn phải nhập từ khóa để tìm kiếm"


def refine_query(query):
    query = query.strip()
    query = query.replace("    ", "  ")
    query = query.replace("   ", "  ")
    query = query.replace("  ", " ")
    return query


def post_process(item):
    item.pop('_id', None) # Remove key '_id' in MongoDB item
    item.pop('text', None)
    return item


class MongoDocItem:
    def __init__(self, doc_id, gov_file_id, text_content):
        self.doc_id = doc_id
        self.gov_file_id = gov_file_id
        self.text = text_content

    def to_dict(self):
        result = {
            "doc_id": self.doc_id,
            "gov_file_id": self.gov_file_id,
            "text": self.text
        }
        return result
    

class FullTextSearchView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    parser_classes = [JSONParser]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongo_client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        self.mongo_collection = self.mongo_client[settings.MONGO_DB_NAME][settings.MONGO_FTS_COLLECTION_NAME]

    def find(self, query):
        mongo_query = {"$text": {"$search": query}}
        search_cursor = self.mongo_collection.find(mongo_query)
        search_results = [post_process(result) for result in search_cursor]
        return search_results

    def post(self, request, *args, **kwargs):
        query = request.data.get('query')
        
        if not query:
            return error_response(1, ERR_MESSAGE_NO_KEYWORD)
        
        query = refine_query(query)
        search_results = self.find(query)
        return list_response(search_results)
        

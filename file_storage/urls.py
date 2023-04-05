from django.urls import path
from .views import DocumentUploadView, GetDocumentByFileId, GetFiles

urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name='upload_document'),
    path('get_doc_by_gov_file_id/', GetDocumentByFileId.as_view(), name='get_document'),
    path('get_files/', GetFiles.as_view(), name='get_files'),
] 

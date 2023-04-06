from django.urls import path
from .views import DocumentUploadView, GetDocumentByGovFileId, GetFiles, DeleteDocumentById

urlpatterns = [
    path('upload_document/', DocumentUploadView.as_view(), name='upload_document'),
    path('get_doc_by_gov_file_id/', GetDocumentByGovFileId.as_view(), name='get_document'),
    path('delete_document_by_id/<int:document_id>/', DeleteDocumentById.as_view(), name='delete_document'),
    path('get_files/', GetFiles.as_view(), name='get_files'),
] 

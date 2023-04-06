from django.urls import path
from views.document import DocumentUploadView, GetDocumentByGovFileId, DeleteDocumentById, UpdateDocumentById
from views.gov_file import GetFiles

urlpatterns = [
    path('upload_document/', DocumentUploadView.as_view(), name='upload_document'),
    path('get_doc_by_gov_file_id/', GetDocumentByGovFileId.as_view(), name='get_document'),
    path('delete_document_by_id/<int:document_id>/', DeleteDocumentById.as_view(), name='delete_document'),
    path('update_document_by_id/<int:document_id>/', UpdateDocumentById.as_view(), name='update_document'),
    path('get_files/', GetFiles.as_view(), name='get_files'),
] 

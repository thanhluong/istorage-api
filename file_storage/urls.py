from django.urls import path
from .views.document import DocumentUploadView, GetDocumentByGovFileId, DeleteDocumentById, UpdateDocumentById
from .views.gov_file import GetGovFiles, CreateGovFile, UpdateGovFileById, DeleteGovFileById

urlpatterns = [
    path('upload_document/', DocumentUploadView.as_view(), name='upload_document'),
    path('get_doc_by_gov_file_id/', GetDocumentByGovFileId.as_view(), name='get_document'),
    path('update_document_by_id/<int:document_id>/', UpdateDocumentById.as_view(), name='update_document'),
    path('delete_document_by_id/<int:document_id>/', DeleteDocumentById.as_view(), name='delete_document'),
    path('get_files/', GetGovFiles.as_view(), name='get_files'),
    path('create_gov_file/', CreateGovFile.as_view(), name='create_file'),
    path('update_gov_file_by_id/<int:gov_file_id>/', UpdateGovFileById.as_view(), name='update_gov_file'),
    path('delete_gov_file_by_id/<int:gov_file_id>/', DeleteGovFileById.as_view(), name='delete_gov_file'),
] 

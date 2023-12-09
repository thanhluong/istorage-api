from django.urls import path
from .views.document import DocumentUploadView, GetDocumentByGovFileId, DeleteDocumentById, UpdateDocumentById
from .views.gov_file import GetGovFiles, CreateGovFile, UpdateGovFileById, UpdateGovFileStateById, DeleteGovFileById
from .views.search import FullTextSearchView
from .views.organ import OrganListApiView, OrganDetailApiView
from .views.organ import OrganDepartmentListApiView, OrganDepartmentDetailApiView, OrganDepartmentByOrganIdListView
from .views.storage_user import StorageUserListApiView, StorageUserDetailApiView, StorageUserByDepartmentListView

urlpatterns = [
    # User APIs,
    path('user', StorageUserListApiView.as_view(), name='user'),
    path('user/user_id/<int:user_id>', StorageUserDetailApiView.as_view(), name='user_detail'),
    path('user/by_department/<int:department_id>', StorageUserByDepartmentListView.as_view(), name='user_by_department'),

    # Doc APIs
    path('upload_document/', DocumentUploadView.as_view(), name='upload_document'),
    path('get_doc_by_gov_file_id/', GetDocumentByGovFileId.as_view(), name='get_doc_by_gov_file_id'),
    path('update_document_by_id/', UpdateDocumentById.as_view(), name='update_document'),
    path('delete_document_by_id/', DeleteDocumentById.as_view(), name='delete_document'),
    path('get_gov_files/', GetGovFiles.as_view(), name='get_files'),
    
    # GovFile APIs
    path('create_gov_file/', CreateGovFile.as_view(), name='create_file'),
    path('update_gov_file_by_id/', UpdateGovFileById.as_view(), name='update_gov_file'),
    path('update_gov_file_state_by_id/', UpdateGovFileStateById.as_view(),
         name='update_gov_file_state'),
    path('delete_gov_file_by_id/', DeleteGovFileById.as_view(), name='delete_gov_file'),

    # Organ APIs
    path('organ', OrganListApiView.as_view(), name='organ'),
    path('organ/<int:organ_id>', OrganDetailApiView.as_view(), name='organ_detail'),
    # OrganDepartment APIs
    path('organ_department', OrganDepartmentListApiView.as_view(), name='organ_department'),
    path('organ_department/<int:organ_department_id>', OrganDepartmentDetailApiView.as_view(), name='organ_department_detail'),
    path('organ_department/by_organ/<int:organ_id>', OrganDepartmentByOrganIdListView.as_view(), name='organ_department_by_organ'),

    # Full-text search APIs
    path('search/', FullTextSearchView.as_view(), name='full_text_search'),
] 

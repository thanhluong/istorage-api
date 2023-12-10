from django.urls import path
from .views.document import DocumentUploadView, GetDocumentByGovFileId, DeleteDocumentById, UpdateDocumentById
from .views.gov_file import GetGovFiles, CreateGovFile, UpdateGovFileById, UpdateGovFileStateById, DeleteGovFileById
from .views.search import FullTextSearchView
from .views.organ import OrganListApiView, OrganDetailApiView
from .views.organ import OrganDepartmentListApiView, OrganDepartmentDetailApiView, OrganDepartmentByOrganIdListView
from .views.organ import OrganRoleListApiView, OrganRoleDetailApiView, OrganRoleByOrganIdListApiView
from .views.organ import PhongListApiView, PhongDetailApiView, PhongByOrganIdListApiView
from .views.storage_user import StorageUserListApiView, StorageUserDetailApiView, StorageUserByDepartmentListView
from .views.storage_user import StorageUserLoginView, StorageUserLogoutView
from .views.storage_user import StorageUserInfoView, StorageUserSetPasswordView
from .views.gov_file_attr import StorageDurationListView, StorageDurationDetailView

urlpatterns = [
    # User APIs,
    path('user', StorageUserListApiView.as_view(), name='user'),
    path('user/user_id/<int:user_id>', StorageUserDetailApiView.as_view(), name='user_detail'),
    path('user/by_department/<int:department_id>', StorageUserByDepartmentListView.as_view(), name='user_by_department'),
    path('user/login', StorageUserLoginView.as_view(), name='user_login'),
    path('user/logout', StorageUserLogoutView.as_view(), name='user_logout'),
    path('user/info', StorageUserInfoView.as_view(), name='user_info'),
    path('user/set_password/<int:user_id>', StorageUserSetPasswordView.as_view(), name='user_set_password'),

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
    # OrganRole APIs
    path('organ_role', OrganRoleListApiView.as_view(), name='organ_role'),
    path('organ_role/<int:organ_role_id>', OrganRoleDetailApiView.as_view(), name='organ_role_detail'),
    path('organ_role/by_organ/<int:organ_id>', OrganRoleByOrganIdListApiView.as_view(), name='organ_role_by_organ'),
    # Fond APIs
    path('fond', PhongListApiView.as_view(), name='phong'),
    path('fond/<int:fond_id>', PhongDetailApiView.as_view(), name='phong_detail'),
    path('fond/by_organ/<int:organ_id>', PhongByOrganIdListApiView.as_view(), name='phong_by_organ'),

    # StorageDuration APIs
    path('storage_duration', StorageDurationListView.as_view(), name='storage_duration'),
    path('storage_duration/<int:storage_duration_id>', StorageDurationDetailView.as_view(), name='storage_duration_detail'),

    # Full-text search APIs
    path('search/', FullTextSearchView.as_view(), name='full_text_search'),
] 

from django.urls import path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views.document import DocumentUploadView, GetDocumentByGovFileId, DeleteDocumentById, UpdateDocumentById
from .views.document import DisplayPdfView
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
from .views.gov_file_attr import PhysicalStateListView, PhysicalStateDetailView
from .views.gov_file_attr import GovFileLanguageListView, GovFileLanguageDetailView
from .views.gov_file_attr import CategoryFileListView, CategoryFileDetailView, CategoryFileByOrganListView
from .views.plan import PlanListView, PlanDetailView, PlanByTypeListView
from .views.plan import SetPlanView, RemovePlanView, SetPlanTieuHuyView, RemovePlanTieuHuyView
from .views.storage_unit import WarehouseListView, WarehouseDetailView, WarehouseByOrganIdListView
from .views.storage_unit import WarehouseRoomListView, WarehouseRoomDetailView, WarehouseRoomByWarehouseIdListView
from .views.storage_unit import ShelfListView, ShelfDetailView, ShelfByWarehouseRoomIdListView
from .views.storage_unit import DrawerListView, DrawerDetailView, DrawerByShelfIdListView, DrawerAssignmentView
from .views.eoffice import EofficeLoginView, EofficeDocumentListView, EofficeAttachmentListView
from .views.eoffice import EofficeAttachmentDownloadView
from .views.khaithac import KhaithacGovFileListView

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny, permissions.IsAuthenticated],
)


urlpatterns = [
    # Swagger views
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

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
    path('display_pdf/<int:gov_file_id>/<int:doc_id>', DisplayPdfView.as_view(), name='display_pdf'),
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

    # PhysicalState APIs
    path('physical_state', PhysicalStateListView.as_view(), name='physical_state'),
    path('physical_state/<int:physical_state_id>', PhysicalStateDetailView.as_view(), name='physical_state_detail'),

    # GovFileLanguage APIs
    path('language', GovFileLanguageListView.as_view(), name='gov_file_language'),
    path('language/<int:gov_file_language_id>', GovFileLanguageDetailView.as_view(), name='gov_file_language_detail'),

    # CategoryFile APIs
    path('category_file', CategoryFileListView.as_view(), name='category_file'),
    path('category_file/<int:category_file_id>', CategoryFileDetailView.as_view(), name='category_file_detail'),
    path('category_file/by_organ/<int:organ_id>', CategoryFileByOrganListView.as_view(), name='category_file_by_organ'),

    # Plan APIs
    path('plan', PlanListView.as_view(), name='plan'),
    path('plan/<int:plan_id>', PlanDetailView.as_view(), name='plan_detail'),
    path('plan/by_type/<int:plan_type>', PlanByTypeListView.as_view(), name='plan_by_type'),
    path('plan/set_plan', SetPlanView.as_view(), name='set_plan'), # Luu Tru Lich Su
    path('plan/remove_plan', RemovePlanView.as_view(), name='remove_plan'),
    path('plan/set_plan_tieuhuy', SetPlanTieuHuyView.as_view(), name='set_plan_tieuhuy'), # Tieu Huy
    path('plan/remove_plan_tieuhuy', RemovePlanTieuHuyView.as_view(), name='remove_plan_tieuhuy'),


    # Warehouse APIs
    path('warehouse', WarehouseListView.as_view(), name='warehouse'),
    path('warehouse/<int:warehouse_id>', WarehouseDetailView.as_view(), name='warehouse_detail'),
    path('warehouse/by_organ/<int:organ_id>', WarehouseByOrganIdListView.as_view(), name='warehouse_by_organ'),

    # WarehouseRoom APIs
    path('warehouse_room', WarehouseRoomListView.as_view(), name='warehouse_room'),
    path('warehouse_room/<int:warehouse_room_id>', WarehouseRoomDetailView.as_view(), name='warehouse_room_detail'),
    path('warehouse_room/by_warehouse/<int:warehouse_id>', WarehouseRoomByWarehouseIdListView.as_view(), name='warehouse_room_by_warehouse'),

    # Shelf APIs
    path('shelf', ShelfListView.as_view(), name='shelf'),
    path('shelf/<int:shelf_id>', ShelfDetailView.as_view(), name='shelf_detail'),
    path('shelf/by_warehouse_room/<int:warehouse_room_id>', ShelfByWarehouseRoomIdListView.as_view(), name='shelf_by_warehouse_room'),

    # Drawer APIs
    path('drawer', DrawerListView.as_view(), name='drawer'),
    path('drawer/<int:drawer_id>', DrawerDetailView.as_view(), name='drawer_detail'),
    path('drawer/by_shelf/<int:shelf_id>', DrawerByShelfIdListView.as_view(), name='drawer_by_shelf'),
    path('set_drawer', DrawerAssignmentView.as_view(), name='set_drawer'),

    # Full-text search APIs
    path('search/', FullTextSearchView.as_view(), name='full_text_search'),

    # e-Office APIs
    path('eoffice/login/<str:username>/<str:password>', EofficeLoginView.as_view(), name='eoffice_login'),
    path('eoffice/document_list', EofficeDocumentListView.as_view(), name='eoffice_document_list'),
    path('eoffice/attachment_list/<str:document_id>', EofficeAttachmentListView.as_view(), name='eoffice_attachment_list'),
    path('eoffice/attachment_download/<str:attachment_id>', EofficeAttachmentDownloadView.as_view(), name='eoffice_attachment_download'),

    # KhaiThac APIs
    path('khaithac/get_gov_files/', KhaithacGovFileListView.as_view(), name='khaithac_get_files'),
] 

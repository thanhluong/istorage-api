from django.db import models
from enum import Enum
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


def menu_icon_path(instance, filename):
    return 'menu_icon/{0}'.format(filename)


def plan_directory_path(instance, filename):
    folder_name = abs(hash(instance.name)) + 2023
    return 'plan/{0}/{1}'.format(folder_name, filename)


class Organ(models.Model):
    storage = models.BooleanField(default=False, null=True, verbose_name="Lưu trữ")
    name = models.CharField(
        max_length=256,
        verbose_name='Tên cơ quan'
    )
    code = models.CharField(
        max_length=64,
        verbose_name="Mã cơ quan"
    )
    address = models.TextField(
        blank=True,
        verbose_name='Địa chỉ'
    )
    phone = models.CharField(
        max_length=64,
        blank=True,
        verbose_name='Số điện thoại'
    )
    fax = models.CharField(
        max_length=64,
        blank=True,
        verbose_name='Số fax'
    )
    provinceName = models.CharField(
        default="Tỉnh Quảng Ngãi",
        max_length=64,
        blank=True,
        verbose_name='Tỉnh thành'
    )
    province = models.IntegerField(
        default=51,
        blank=True,
        null=True,
        verbose_name='ID tỉnh thành'
    )
    districtName = models.CharField(
        default="Thành phố Quảng Ngãi",
        max_length=64,
        blank=True,
        verbose_name='Quận huyện'
    )
    district = models.IntegerField(
        default=522,
        blank=True,
        null=True,
        verbose_name='ID quận huyện'
    )
    wardName = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        default=None,
        verbose_name='Phường xã'
    )
    ward = models.IntegerField(
        blank=True,
        null=True,
        default=None,
        verbose_name='ID phường xã'
    )
    note = models.TextField(
        blank=True,
        default="",
        verbose_name='Ghi chú'
    )

    class Meta:
        verbose_name = 'Cơ quan'
        verbose_name_plural = 'Cơ quan'

    def __str__(self):
        return self.name


class OrganDepartment(models.Model):
    organ = models.ForeignKey(
        Organ,
        on_delete=models.CASCADE,
        verbose_name='Cơ quan'
    )
    name = models.CharField(
        max_length=256,
        verbose_name='Tên phòng ban'
    )
    code = models.CharField(
        max_length=84,
        verbose_name="Mã phòng ban"
    )

    class Meta:
        verbose_name = 'Phòng ban'
        verbose_name_plural = 'Phòng ban'

    def __str__(self):
        return self.name


class OrganRole(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Tên chức vụ'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Mô tả'
    )
    organ = models.ForeignKey(
        Organ,
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE,
        verbose_name='Cơ quan'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Chức vụ trong cơ quan'
        verbose_name_plural = 'Chức vụ trong cơ quan'


class StorageUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=84, unique=True, verbose_name="Email")
    username = models.CharField(max_length=64, unique=True, verbose_name="Tên đăng nhập")
    full_name = models.CharField(max_length=64, blank=True, verbose_name="Họ và tên")
    phone = models.CharField(max_length=32, blank=True, verbose_name="Số điện thoại")
    is_staff = models.BooleanField(default=False, verbose_name="Quản trị cơ quan")
    is_superuser = models.BooleanField(default=False, verbose_name="Quản trị hệ thống")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    is_archive_staff = models.BooleanField(default=False, verbose_name="Nhân viên lưu trữ LS")

    first_name = models.CharField(max_length=64, blank=True, verbose_name="Tên đệm và tên")
    last_name = models.CharField(max_length=32, blank=True, verbose_name="Họ")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tham gia")
    last_login = models.DateTimeField(auto_now=True, verbose_name="Lần đăng nhập cuối")

    department = models.ForeignKey(
        OrganDepartment,
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE,
        verbose_name='Phòng ban',
    )
    role = models.ForeignKey(
        OrganRole,
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE,
        verbose_name='Chức vụ',
    )
    menu_permission = models.CharField(
        max_length=640,
        blank=True,
        verbose_name="Các menu được truy cập"
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Người dùng hệ thống'
        verbose_name_plural = 'Người dùng hệ thống'

    def __str__(self):
        return self.username


class Phong(models.Model):
    fond_name = models.CharField(max_length=256, verbose_name='Tên phông')
    fond_history = models.CharField(
        max_length=640,
        blank=True,
        null=True,
        default="",
        verbose_name='Lịch sử đơn vị hình thành phông'
    )
    archives_time = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        default="",
        verbose_name='Thời gian tài liệu'
    )

    identifier = models.CharField(max_length=64, verbose_name="Mã phông")
    organ = models.ForeignKey(
        Organ,
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET(None),
        verbose_name='Mã cơ quan lưu trữ'
    )

    class Meta:
        verbose_name = 'Phông lưu trữ'
        verbose_name_plural = 'Phông lưu trữ'

    def __str__(self):
        return self.fond_name


class CategoryFile(models.Model):
    name = models.CharField(max_length=512, verbose_name='Tên danh mục')
    order = models.IntegerField(default=1, verbose_name='Order')
    organ = models.ForeignKey(
        Organ,
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET(None),
        verbose_name='Cơ quan'
    )
    parent = models.ForeignKey(
        'self',
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET(None),
        verbose_name='Danh mục cha'
    )

    class Meta:
        verbose_name = 'Danh mục hồ sơ'
        verbose_name_plural = 'Danh mục hồ sơ'

    def __str__(self):
        return self.name


class GovFileLanguage(models.Model):
    name = models.CharField(max_length=128, verbose_name='Tên ngôn ngữ')
    code = models.CharField(max_length=16, verbose_name='Mã ngôn ngữ')

    class Meta:
        verbose_name = 'Ngôn ngữ'
        verbose_name_plural = 'Ngôn ngữ'

    def __str__(self):
        return self.name


class PhysicalState(models.Model):
    name = models.CharField(max_length=128, verbose_name='Tên tình trạng vật lý')
    code = models.CharField(max_length=64, verbose_name='Mã tình trạng vật lý')

    class Meta:
        verbose_name = 'Tình trạng vật lý'
        verbose_name_plural = 'Tình trạng vật lý'

    def __str__(self):
        return self.name


class StorageDuration(models.Model):
    duration = models.CharField(max_length=128, verbose_name='Tên thời hạn bảo quản')
    code = models.CharField(max_length=64, verbose_name='Mã thời hạn bảo quản')
    number_of_year = models.IntegerField(verbose_name='Số năm')

    class Meta:
        verbose_name = 'Thời hạn bảo quản'
        verbose_name_plural = 'Thời hạn bảo quản'

    def __str__(self):
        return self.duration


class Plan(models.Model):
    STATE_CHOICE = (
        ("Mới lập", "Mới lập"),
        ("Đợi duyệt", "Đợi duyệt"),
        ("Đã duyệt", "Đã duyệt"),
        ("Trả về", "Trả về"),
        ("Đợi Sở Nội vụ duyệt", "Đợi Sở Nội vụ duyệt"),
    )

    name = models.CharField(
        max_length=512,
        verbose_name='Tên kế hoạch'
    )
    start_date = models.DateField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Thời gian bắt đầu'
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Thời gian kết thúc'
    )
    organ = models.ForeignKey(
        Organ,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET(None),
        verbose_name='Cơ quan'
    )
    state = models.CharField(
        max_length=64,
        choices=STATE_CHOICE,
        verbose_name='Trạng thái'
    )
    type = models.IntegerField(
        choices=[
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4)
        ],
        default=1,
        verbose_name='Loại kế hoạch'
    )
    attachment = models.FileField(
        blank=True,
        null=True,
        default=None,
        upload_to=plan_directory_path
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kế hoạch'
        verbose_name_plural = 'Kế hoạch'


class GovFile(models.Model):
    gov_file_code = models.CharField(max_length=100, blank=True, null=True)
    organ_id = models.ForeignKey(
        Phong,
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET(None),
        verbose_name='Phông lưu trữ lịch sử'
    )
    identifier = models.ForeignKey(
        Organ,
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET(None),
        verbose_name='Cơ quan lưu trữ'
    )
    category_file = models.ForeignKey(
        CategoryFile,
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET(None),
        verbose_name='Danh mục hồ sơ'
    )
    on_trash = models.BooleanField(default=False)
    file_catalog = models.IntegerField(blank=True, null=True)
    file_notation = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Tiêu đề')
    maintenance = models.ForeignKey(
        StorageDuration,
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET(None),
        verbose_name='Thời hạn bảo quản'
    )
    rights = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Chế độ sử dụng"
    )
    language = models.ForeignKey(
        GovFileLanguage,
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET(None),
        verbose_name='Ngôn ngữ'
    )
    start_date = models.DateField(blank=True, null=True, verbose_name='Ngày bắt đầu')
    end_date = models.DateField(blank=True, null=True, verbose_name='Ngày kết thúc')
    total_doc = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    infor_sign = models.CharField(max_length=100, blank=True, null=True, verbose_name='Bút tích')
    keyword = models.CharField(max_length=100, blank=True, null=True)
    sheet_number = models.IntegerField(blank=True, null=True)
    page_number = models.IntegerField(blank=True, null=True)
    format = models.ForeignKey(
        PhysicalState,
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET(None),
        verbose_name='Tình trạng vật lý'
    )
    extra_info = models.TextField(blank=True, null=True)

    plan_thuthap = models.ForeignKey(
        Plan,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET(None),
        related_name="thuthapnopluu",
        verbose_name='Nằm trong kế hoạch thu thập'
    )

    plan_bmcl = models.ForeignKey(
        Plan,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET(None),
        related_name="bienmucchinhly",
        verbose_name='Nằm trong kế hoạch biên mục chỉnh lý'
    )

    plan_nopluuls = models.ForeignKey(
        Plan,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET(None),
        related_name="nopluulichsu",
        verbose_name='Nằm trong kế hoạch nộp lưu LS'
    )

    plan_tieuhuy = models.ForeignKey(
        Plan,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET(None),
        related_name="tieuhuy",
        verbose_name='Nằm trong kế hoạch tiêu huỷ'
    )

    drawer = models.ForeignKey(
        'Drawer',
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET(None),
        verbose_name='Hộp lưu trữ'
    )

    def __str__(self):
        return 'Hồ sơ: ' + self.title

    class Meta:
        verbose_name = 'Hồ sơ'
        verbose_name_plural = 'Hồ sơ'


class Document(models.Model):
    doc_code = models.CharField(max_length=100, blank=True, null=True)
    gov_file_id = models.CharField(max_length=100, blank=True, null=True)
    identifier = models.CharField(max_length=100, blank=True, null=True)
    organ_id = models.CharField(max_length=100, blank=True, null=True)
    file_catalog = models.IntegerField(blank=True, null=True)
    file_notation = models.CharField(max_length=200, blank=True, null=True)
    doc_ordinal = models.IntegerField(blank=True, null=True)
    type_name = models.CharField(max_length=100, blank=True, null=True)
    code_number = models.CharField(max_length=100, blank=True, null=True)
    code_notation = models.CharField(max_length=300, blank=True, null=True)
    issued_date = models.DateField(blank=True, null=True)
    organ_name = models.CharField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=500, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    page_amount = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    infor_sign = models.CharField(max_length=100, blank=True, null=True)
    keyword = models.CharField(max_length=100, blank=True, null=True)
    mode = models.CharField(max_length=100, blank=True, null=True)
    confidence_level = models.CharField(max_length=100, blank=True, null=True)
    autograph = models.CharField(max_length=2000, blank=True, null=True)
    format = models.CharField(max_length=100, blank=True, null=True)
    doc_name = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return 'Văn bản: ' + self.doc_name

    class Meta:
        verbose_name = 'Văn bản'
        verbose_name_plural = 'Văn bản'


class StateEnum(Enum):
    OPEN = 1
    CLOSE = 2
    SUBMIT_ORGAN = 3
    STORE_ORGAN = 4
    SUBMIT_ARCHIVE = 5
    STORE_ARCHIVE = 6
    RETURN = 7
    RETURN_ARCHIVE = 8
    DA_NHAN_NOP_LUU = 9
    CHO_XEP_KHO = 10
    HSCL_TAO_MOI = 11
    HSCL_GIAO_NOP = 12
    HSCL_BI_TRA_VE = 13
    THHS_CHO_TIEU_HUY = 14
    THHS_CHO_PHE_DUYET_TIEU_HUY = 15
    THHS_DA_TIEU_HUY = 16
    THHS_KHOI_PHUC = 17
    NOP_LUU_LICH_SU_CHO_SO_NOI_VU_DUYET = 18

    @classmethod
    def choices(cls):
        return [(member.value, name) for name, member in cls.__members__.items()]


class GovFileProfile(models.Model):
    gov_file_id = models.IntegerField()
    state = models.IntegerField(choices=StateEnum.choices())

    class Meta:
        verbose_name = 'Trạng thái hồ sơ'
        verbose_name_plural = 'Trạng thái hồ sơ'


class SiteMenu(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Tiêu đề menu'
    )
    url = models.CharField(
        max_length=256,
        blank=True,
        verbose_name='Đường dẫn'
    )
    parent_id = models.CharField(
        max_length=128,
        blank=True,
        verbose_name="Tên menu cha"
    )
    icon = models.ImageField(
        blank=True,
        null=True,
        upload_to=menu_icon_path,
        verbose_name="Biểu tượng cho menu"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menu'


class OrganTemplate(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Tên mẫu'
    )
    organ_name = models.CharField(
        max_length=256,
        verbose_name='Tên cơ quan'
    )
    param1 = models.CharField(
        max_length=64,
        blank=True,
        verbose_name='Tham số 1'
    )
    param2 = models.CharField(
        max_length=64,
        blank=True,
        verbose_name='Tham số 2'
    )
    content = models.TextField(
        blank=True,
        verbose_name='Nội dung template'
    )

    def __str__(self):
        return "Template: " + self.name

    class Meta:
        verbose_name = 'Template cơ quan'
        verbose_name_plural = 'Template cơ quan'


class DocumentSecurityLevel(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name='Tên mức độ bảo mật'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Mô tả'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Cấp độ bảo mật'
        verbose_name_plural = 'Cấp độ bảo mật'


class Warehouse(models.Model):
    organ = models.ForeignKey(
        Organ,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET(None),
        verbose_name='Cơ quan'
    )
    state = models.BooleanField(default=True, verbose_name="Trạng thái kho")
    name = models.CharField(
        max_length=256,
        verbose_name='Tên kho'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lưu trữ - Kho'
        verbose_name_plural = 'Lưu trữ - Kho'


class WarehouseRoom(models.Model):
    warehouse = models.ForeignKey(
        Warehouse,
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE,
        verbose_name='Kho'
    )

    state = models.BooleanField(default=True, verbose_name="Trạng thái phòng kho")
    name = models.CharField(
        max_length=256,
        verbose_name='Tên phòng kho'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lưu trữ - Phòng kho'
        verbose_name_plural = 'Lưu trữ - Phòng kho'


class Shelf(models.Model):
    warehouse_room = models.ForeignKey(
        WarehouseRoom,
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE,
        verbose_name='Phòng kho'
    )

    state = models.BooleanField(default=True, verbose_name="Trạng thái kệ")
    name = models.CharField(
        max_length=256,
        verbose_name='Tên kệ'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lưu trữ - Kệ'
        verbose_name_plural = 'Lưu trữ - Kệ'


class Drawer(models.Model):
    shelf = models.ForeignKey(
        Shelf,
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE,
        verbose_name='Kệ'
    )

    state = models.BooleanField(default=True, verbose_name="Trạng thái hộp")
    name = models.CharField(
        max_length=256,
        verbose_name='Tên hộp'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lưu trữ - Hộp'
        verbose_name_plural = 'Lưu trữ - Hộp'
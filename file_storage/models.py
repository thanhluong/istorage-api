from django.db import models
from enum import Enum


def menu_icon_path(instance, filename):
    return 'menu_icon/{0}'.format(filename)


class GovFile(models.Model):
    gov_file_code = models.CharField(max_length=100, blank=True, null=True)
    identifier = models.CharField(max_length=100, blank=True, null=True)
    organ_id = models.CharField(max_length=100, blank=True, null=True)
    file_catalog = models.IntegerField(blank=True, null=True)
    file_notation = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    maintenance = models.CharField(max_length=100, blank=True, null=True)
    rights = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    total_doc = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    infor_sign = models.CharField(max_length=100, blank=True, null=True)
    keyword = models.CharField(max_length=100, blank=True, null=True)
    sheet_number = models.IntegerField(blank=True, null=True)
    page_number = models.IntegerField(blank=True, null=True)
    format = models.CharField(max_length=100, blank=True, null=True)
    extra_info = models.TextField(blank=True, null=True)

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


class OrganRole(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Tên chức vụ'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Mô tả'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Chức vụ trong cơ quan'
        verbose_name_plural = 'Chức vụ trong cơ quan'


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
        verbose_name='Phường xã'
    )
    ward = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='ID phường xã'
    )

    def __str__(self):
        return self.name


class Plan(models.Model):
    STATE_CHOICE = (
        ("Mới lập", "Mới lập"),
        ("Đợi duyệt", "Đợi duyệt"),
        ("Đã duyệt", "Đã duyệt"),
        ("Trả về", "Trả về"),
    )

    name = models.CharField(
        max_length=128,
        verbose_name='Tên kế hoạch'
    )
    date = models.DateField(
        verbose_name='Thời gian'
    )
    organ_id = models.IntegerField(
        default=1,
        verbose_name='ID cơ quan'
    )
    state = models.CharField(
        max_length=64,
        choices=STATE_CHOICE,
        verbose_name='Trạng thái'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kế hoạch'
        verbose_name_plural = 'Kế hoạch'

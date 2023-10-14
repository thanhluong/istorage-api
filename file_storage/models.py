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

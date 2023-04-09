from django.db import models
from enum import Enum


class GovFile(models.Model):
    gov_file_code = models.CharField(max_length=100)
    identifier = models.CharField(max_length=13, null=True)
    organ_id = models.CharField(max_length=13, null=True)
    file_catalog = models.IntegerField(null=True)
    file_notation = models.CharField(max_length=20, null=True)
    title = models.CharField(max_length=1000, null=True)
    maintenance = models.CharField(max_length=100, null=True)
    rights = models.CharField(max_length=30, null=True)
    language = models.CharField(max_length=100, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    total_doc = models.IntegerField(null=True)
    description = models.CharField(max_length=2000, null=True)
    infor_sign = models.CharField(max_length=30, null=True)
    keyword = models.CharField(max_length=100, null=True)
    sheet_number = models.IntegerField(null=True)
    page_number = models.IntegerField(null=True)
    format = models.CharField(max_length=50, null=True)
    extra_info = models.TextField(null=True)


class Document(models.Model):
    doc_code = models.CharField(max_length=13, null=True)
    gov_file_id = models.CharField(max_length=13, null=True)
    identifier = models.CharField(max_length=13, null=True)
    organ_id = models.CharField(max_length=13, null=True)
    file_catalog = models.IntegerField(null=True)
    file_notation = models.CharField(max_length=20, null=True)
    doc_ordinal = models.IntegerField(null=True)
    type_name = models.CharField(max_length=100, null=True)
    code_number = models.CharField(max_length=11, null=True)
    code_notation = models.CharField(max_length=30, null=True)
    issued_date = models.DateField(null=True)
    organ_name = models.CharField(max_length=200, null=True)
    subject = models.CharField(max_length=500, null=True)
    language = models.CharField(max_length=100, null=True)
    page_amount = models.IntegerField(null=True)
    description = models.CharField(max_length=500, null=True)
    infor_sign = models.CharField(max_length=30, null=True)
    keyword = models.CharField(max_length=100, null=True)
    mode = models.CharField(max_length=20, null=True)
    confidence_level = models.CharField(max_length=30, null=True)
    autograph = models.CharField(max_length=2000, null=True)
    format = models.CharField(max_length=50, null=True)
    doc_name = models.CharField(max_length=256, null=True)


class StateEnum(Enum):
    OPEN = 1
    CLOSE = 2
    SUBMIT_ORGAN = 3
    STORE_ORGAN = 4
    SUBMIT_ARCHIVE = 5
    STORE_ARCHIVE = 6

    @classmethod
    def choices(cls):
        return [(member.value, name) for name, member in cls.__members__.items()]


class GovFileProfile(models.Model):
    gov_file_id = models.IntegerField()
    state = models.IntegerField(choices=StateEnum.choices())

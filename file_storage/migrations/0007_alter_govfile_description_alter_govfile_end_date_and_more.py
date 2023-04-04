# Generated by Django 4.2 on 2023-04-04 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_storage', '0006_alter_govfile_identifier_alter_govfile_organ_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='govfile',
            name='description',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='govfile',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='govfile',
            name='extra_info',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='govfile',
            name='file_notation',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='govfile',
            name='format',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='govfile',
            name='infor_sign',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='govfile',
            name='keyword',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='govfile',
            name='language',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='govfile',
            name='maintenance',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='govfile',
            name='rights',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='govfile',
            name='start_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='govfile',
            name='title',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]

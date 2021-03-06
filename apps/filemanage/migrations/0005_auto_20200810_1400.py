# Generated by Django 3.1 on 2020-08-10 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('filemanage', '0004_folderinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folderinfo',
            name='createdBy',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='folderinfo_created_by', to=settings.AUTH_USER_MODEL, verbose_name='创建人ID'),
        ),
        migrations.AlterField(
            model_name='folderinfo',
            name='updatedBy',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='folderinfo_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='修改人ID'),
        ),
        migrations.CreateModel(
            name='FileInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='创建时间')),
                ('updateTime', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='修改时间')),
                ('deletedTime', models.DateTimeField(blank=True, default=None, null=True, verbose_name='删除时间')),
                ('isActive', models.BooleanField(default=True, verbose_name='是否正常')),
                ('file_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='文件名称')),
                ('createdBy', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fileinfo_created_by', to=settings.AUTH_USER_MODEL, verbose_name='创建人ID')),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='filemanage.folderinfo', verbose_name='文件夹')),
                ('updatedBy', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fileinfo_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='修改人ID')),
            ],
            options={
                'verbose_name': '文件信息',
                'verbose_name_plural': '文件信息',
            },
        ),
    ]

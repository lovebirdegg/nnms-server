# Generated by Django 3.1 on 2020-08-18 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='创建时间')),
                ('updateTime', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='修改时间')),
                ('deletedTime', models.DateTimeField(blank=True, default=None, null=True, verbose_name='删除时间')),
                ('isActive', models.BooleanField(default=True, verbose_name='是否正常')),
                ('category_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='栏目名称')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('createdBy', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categoryinfo_created_by', to=settings.AUTH_USER_MODEL, verbose_name='创建人ID')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='cms.categoryinfo', verbose_name='栏目目录')),
                ('updatedBy', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categoryinfo_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='修改人ID')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

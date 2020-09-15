# Generated by Django 2.1.7 on 2020-07-24 11:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='创建时间')),
                ('updateTime', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='修改时间')),
                ('deletedTime', models.DateTimeField(blank=True, default=None, null=True, verbose_name='删除时间')),
                ('createdBy', models.IntegerField(default=0, null=True, verbose_name='创建人ID')),
                ('updatedBy', models.IntegerField(default=0, null=True, verbose_name='修改人ID')),
                ('isActive', models.BooleanField(default=True, verbose_name='是否正常')),
                ('hostname', models.CharField(max_length=50, verbose_name='IP/域名')),
                ('code', models.CharField(max_length=50, verbose_name='设备编码')),
                ('buy_date', models.DateField(default=django.utils.timezone.now, verbose_name='购买日期')),
                ('warranty_date', models.DateField(default=django.utils.timezone.now, verbose_name='到保日期')),
                ('desc', models.TextField(blank=True, default='', verbose_name='备注信息')),
                ('longitude', models.CharField(max_length=100, verbose_name='经度')),
                ('latitude', models.CharField(max_length=100, verbose_name='纬度')),
            ],
            options={
                'verbose_name': '设备信息',
                'verbose_name_plural': '设备信息',
            },
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='创建时间')),
                ('updateTime', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='修改时间')),
                ('deletedTime', models.DateTimeField(blank=True, default=None, null=True, verbose_name='删除时间')),
                ('createdBy', models.IntegerField(default=0, null=True, verbose_name='创建人ID')),
                ('updatedBy', models.IntegerField(default=0, null=True, verbose_name='修改人ID')),
                ('isActive', models.BooleanField(default=True, verbose_name='是否正常')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('code', models.CharField(max_length=50, verbose_name='编码')),
                ('desc', models.TextField(blank=True, default='', verbose_name='备注信息')),
            ],
            options={
                'verbose_name': '设备类型',
                'verbose_name_plural': '设备类型',
            },
        ),
        migrations.AddField(
            model_name='deviceinfo',
            name='device_type',
            field=models.ManyToManyField(blank=True, to='rmms.DeviceType', verbose_name='设备类型'),
        ),
    ]
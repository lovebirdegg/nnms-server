# Generated by Django 3.1 on 2020-08-11 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filemanage', '0007_fileinfo_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileinfo',
            name='size',
            field=models.BigIntegerField(blank=True, default=0, null=True, verbose_name='文件大小'),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='extension',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='扩展名'),
        ),
    ]

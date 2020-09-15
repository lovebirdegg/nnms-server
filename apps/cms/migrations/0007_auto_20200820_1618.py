# Generated by Django 3.1 on 2020-08-20 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_auto_20200819_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content_display',
            field=models.BooleanField(default=True, verbose_name='是否显示'),
        ),
        migrations.AlterField(
            model_name='content',
            name='content_type',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='文章类型'),
        ),
    ]

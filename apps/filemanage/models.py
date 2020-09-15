from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import os
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
# Create your models here.
class SoftDeletableQuerySet(models.query.QuerySet):
    def delete(self):
        self.update(deletedTime=timezone.now())

class SoftDeletableManager(models.Manager):
    """
    仅返回未被删除的实例
    """
    _queryset_class = SoftDeletableQuerySet

    def get_queryset(self):
        """
        在这里处理一下QuerySet, 然后返回没被标记位is_deleted的QuerySet
        """
        kwargs = {'model': self.model, 'using': self._db}
        if hasattr(self, '_hints'):
            kwargs['hints'] = self._hints

        return self._queryset_class(**kwargs).filter(deletedTime=None)

class BaseModel(models.Model):
    """
        基础模型
    """
    createTime = models.DateTimeField(verbose_name="创建时间",default=timezone.now,null=True)
    updateTime = models.DateTimeField(verbose_name="修改时间",default=timezone.now,null=True)
    deletedTime = models.DateTimeField("删除时间",null=True, blank=True,default=None)
    # createdBy = models.IntegerField(verbose_name="创建人ID",default=0,null=True)
    createdBy = models.ForeignKey(User, null=True, blank=True, default=1, on_delete=models.SET_NULL, verbose_name='创建人ID', related_name="%(class)s_created_by")
    updatedBy = models.ForeignKey(User, null=True, blank=True, default=1, on_delete=models.SET_NULL, verbose_name='修改人ID', related_name="%(class)s_updated_by")
    # updatedBy = models.IntegerField(verbose_name="修改人ID",default=0,null=True)
    isActive = models.BooleanField(default=True, verbose_name='是否正常')

    objects = SoftDeletableManager()
    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.createdBy = self.user.id
    #     else:
    #         self.updatedBy = self.user.id
        # super().save(*args, **kwargs)
    def delete(self, using=None, soft=True, *args, **kwargs):
        if soft:
            self.deletedTime = timezone.now()
            self.save()
        else:
            return super(SoftDeletableModel, self).delete(using=using, *args, **kwargs)
    class Meta:
        abstract = True


class FolderInfo(MPTTModel,BaseModel):
    '''
    文件夹信息表
    '''
    fold_name = models.CharField(max_length=50, verbose_name='目录名称',null=True, blank=True,)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, verbose_name='上级目录',blank=True, null=True, related_name="children")

    def __unicode__(self):
        return self.fold_name
    class MPTTMeta:
        order_insertion_by = ['id']

class FileInfo(BaseModel):
    '''
    文件信息表
    '''
    file = models.FileField(upload_to='upload', default='')
    original_filename = models.CharField(verbose_name='文件原始名称', max_length=255, blank=True, null=True)
    file_name = models.CharField(max_length=255, verbose_name='文件名称',null=True, blank=True,)
    folder =  models.ForeignKey(FolderInfo, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='文件夹')
    sha1 = models.CharField(verbose_name='sha1', max_length=40, blank=True, default='')
    file_type = models.CharField(max_length=255, verbose_name='文件类型',null=True, blank=True,)
    path = models.CharField(max_length=255, verbose_name='文件路径',null=True, blank=True,)
    
    # def get_size(self):
    #     return self.file.size or 0

    # def get_extension(self):
    #     filetype = os.path.splitext(self.file.name)[1].lower()
    #     if len(filetype) > 0:
    #         filetype = filetype[1:]
    #     return filetype

    size = models.BigIntegerField(verbose_name='文件大小', null=True, blank=True, default=0)
    extension = models.CharField(max_length=255, verbose_name='扩展名',null=True, blank=True,default='')


    class Meta:
        verbose_name = "文件信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
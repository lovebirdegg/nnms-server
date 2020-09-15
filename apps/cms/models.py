from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import os
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()
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
    createdBy = models.ForeignKey(User, null=True, blank=True, default=1, on_delete=models.SET_NULL, verbose_name='创建人ID', related_name="%(class)s_created_by")
    updatedBy = models.ForeignKey(User, null=True, blank=True, default=1, on_delete=models.SET_NULL, verbose_name='修改人ID', related_name="%(class)s_updated_by")
    isActive = models.BooleanField(default=True, verbose_name='是否正常')

    objects = SoftDeletableManager()

    def delete(self, using=None, soft=True, *args, **kwargs):
        if soft:
            self.deletedTime = timezone.now()
            self.save()
        else:
            return super(SoftDeletableModel, self).delete(using=using, *args, **kwargs)
    class Meta:
        abstract = True

class CategoryInfo(MPTTModel,BaseModel):
    '''
    栏目信息表
    '''
    category_name = models.CharField(max_length=50, verbose_name='栏目名称',null=True, blank=True,)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, verbose_name='父栏目',blank=True, null=True, related_name="children")

    def __unicode__(self):
        return self.category_name

    class MPTTMeta:
        order_insertion_by = ['id']

    class Meta:
        verbose_name = '栏目管理'
        verbose_name_plural = '栏目管理'

class Content(BaseModel):

    '''
    内容信息表
    '''
    content_title = models.CharField(max_length=255, verbose_name='文章标题',null=True, blank=True,)
    content_category = models.ForeignKey(CategoryInfo, on_delete=models.SET_NULL, verbose_name='所属栏目',null=True, blank=True,)
    content_url = models.CharField(max_length=255, verbose_name='文章跳转链接地址',null=True, blank=True,)
    content_details = models.TextField(verbose_name='文章内容',null=True, blank=True,)
    content_keyword = models.CharField(max_length=255, verbose_name='关键字',null=True, blank=True,)
    content_description = models.CharField(max_length=400, verbose_name='文章描述',null=True, blank=True,)
    content_img = models.CharField(max_length=255, verbose_name='文章缩略图',null=True, blank=True,)
    content_sort = models.IntegerField(verbose_name='自定义顺序',null=True, blank=True,)
    content_display = models.BooleanField(default=True,verbose_name='是否显示')
    content_type = models.CharField(max_length=255, verbose_name='文章类型',null=True, blank=True,)
    content_pub_datetime = models.DateTimeField(verbose_name="发布时间",default=timezone.now,null=True)
    content_hit = models.IntegerField(verbose_name='点击次数',null=True, blank=True,)

    def __unicode__(self):
        return self.category_name

    class Meta:
        verbose_name = '内容管理'
        verbose_name_plural = '内容管理'

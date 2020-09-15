from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


from django.utils import timezone

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
    createdBy = models.ForeignKey(User, null=True, blank=True, default=1, on_delete=models.SET_NULL, verbose_name='创建人ID', related_name='createdBy')
    updatedBy = models.ForeignKey(User, null=True, blank=True, default=1, on_delete=models.SET_NULL, verbose_name='修改人ID', related_name='updatedBy')
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

class DeviceInfo(BaseModel):
    '''
    设备信息表
    '''
    hostname = models.CharField(max_length=50, verbose_name='IP/域名',null=True, blank=True,)
    code = models.CharField(max_length=50, verbose_name='设备编码')
    device_type = models.CharField(max_length=50,verbose_name="设备类型", blank=True)
    buy_date = models.DateField(default=timezone.now, verbose_name="购买日期")
    warranty_date = models.DateField(default=timezone.now, verbose_name="到保日期")
    desc = models.TextField(blank=True, default='', verbose_name='备注信息')
    longitude=models.CharField(max_length=100, verbose_name='经度',null=True, blank=True,)
    latitude=models.CharField(max_length=100, verbose_name='纬度', null=True, blank=True,)
    class Meta:
        verbose_name = "设备信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
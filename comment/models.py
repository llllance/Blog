
from django.db import models

# Create your models here.

class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),

        (STATUS_DELETE, '删除'),
    )
    target=models.CharField(max_length=100,verbose_name='评论目标')
    content=models.CharField(max_length=2000,verbose_name='内容')
    nickname=models.CharField(max_length=50,verbose_name='昵称')
    website=models.URLField(verbose_name='网站')
    email=models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name='状态')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name='评论'
        verbose_name_plural=verbose_name

    def __str__(self):#不可以返回空，所以返回字段应为not null
        return self.target#target是外键，需要选择外键的一个字段进行返回

    @classmethod
    def get_by_target(cls,target):
        return cls.objects.filter(target=target,status=cls.STATUS_NORMAL)

    @property
    def get_by_post_title(self,target):
        from re import search
        from blog.models import Post
        id=search(r'\d+',target).group()
        title=Post.objects.get(id=id)
        return title
import mistune
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.functional import cached_property


class Category(models.Model):#分类类
    STATUS_NORMAL=1
    STATUS_DELETE=0
    STATUS_ITEMS=(
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除'),
    )
    name=models.CharField(max_length=50,verbose_name='名称')
    status=models.PositiveIntegerField(default=STATUS_NORMAL,
                                       choices=STATUS_ITEMS,verbose_name='状态')
    is_nav=models.BooleanField(default=False,verbose_name="是否为导航")
    owner=models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name='分类'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(self):#分别获取属于导航的类别和普通的类别
        categories=self.objects.filter(status=self.STATUS_NORMAL)
        nav_categories=[]
        normal_categories=[]
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        return {
            'navs':nav_categories,
            'categories':normal_categories,
        }

class Tag (models.Model):#标签类
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name=models.CharField(max_length=10,verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者',on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


    class Meta:
        verbose_name="标签"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):#文章类
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT=2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT,'草稿'),
    )

    title=models.CharField(max_length=255,verbose_name='标题')
    desc=models.CharField(max_length=1024,blank=True,verbose_name='摘要')
    content=models.TextField(verbose_name='正文',help_text='正文必须为MarkDown格式',)
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name='状态')
    category=models.ForeignKey(Category,verbose_name='分类',on_delete=models.DO_NOTHING)
    tag=models.ManyToManyField(Tag,verbose_name='标签')
    owner=models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    pv=models.PositiveIntegerField(default=1)#page view,页面浏览量，一个浏览者浏览了你多少个页面
    uv=models.PositiveIntegerField(default=1)#unique visitor 浏览者数，浏览每个网页的人数

    content_html=models.TextField(verbose_name='正文html代码',blank=True,editable=False)
    is_md=models.BooleanField(default=False,verbose_name='markdown语法')#判断使用富文本还是markdown，通过重写save实现

    def save(self,*args,**kwargs):
        if self.is_md:
            self.content_html=mistune.markdown(self.content)
        else:
            self.content_html=self.content
        super().save(*args,**kwargs)

    class Meta:
        verbose_name='文章'
        verbose_name_plural=verbose_name
        ordering=['-id']#根据ID进行降序排序

    def __str__(self):
        return self.title

    @classmethod
    def hot_posts(cls,with_related=True):#获取最热文章
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv').select_related('owner','category')

    @classmethod
    def latest_posts(cls,with_related=True):#获取最新文章
        queryset=cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-created_time')
        if with_related:#控制返回的数据是否要加上两个外键数据
            queryset=queryset.select_related('owner','category')
        return queryset

    @cached_property#把返回的数据绑定到实例中
    def tags(self):
        return ','.join(self.tag.values_list('name',flat=True))
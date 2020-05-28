from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.template.loader import render_to_string


class Link(models.Model):#友链
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    status=models.PositiveIntegerField(default=STATUS_NORMAL,
                                       choices=STATUS_ITEMS,verbose_name='状态')

    title=models.CharField(max_length=50,verbose_name='标题')
    href=models.URLField(verbose_name='链接',)#默认长度为200
    weight=models.PositiveIntegerField(default=1,choices=zip(range(1,6),range(1,6)),
                                       verbose_name='权重',help_text='权重高的展示顺序靠前')
    owner=models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name='友链'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.title

class SideBar(models.Model):#侧边栏
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, '展示'),
        (STATUS_HIDE, '隐藏'),
    )
    DISPLAY_HTML=1
    DISPLAY_LATEST=2
    DISPLAY_HOT=3
    DISPLAY_COMMENT=4
    SIDE_TYPE=(
        (DISPLAY_HTML,'HTML'),
        (DISPLAY_LATEST,'最新文章'),
        (DISPLAY_HOT,'最热文章'),
        (DISPLAY_COMMENT,'最近评论'),
    )
    title=models.CharField(max_length=50,verbose_name='标题')
    display_type=models.PositiveIntegerField(default=1,choices=SIDE_TYPE,
                                             verbose_name='展示类型')
    content=models.CharField(max_length=500,blank=True,verbose_name='内容',
                             help_text='如果设置的不是HTML类型，可为空')
    status=models.PositiveIntegerField(default=STATUS_SHOW,choices=STATUS_ITEMS,verbose_name='状态')
    owner=models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name='侧边栏'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.title

    @classmethod#函数不需要实例化，不需要self参数，但第一个参数需要是表示自身类的 cls 参数，可以来调用类的属性，类的方法，实例化对象等。
    def get_all(cls):#获取所有侧边栏内容
        return cls.objects.filter(status=cls.STATUS_SHOW)#cls=SideBar

    @property#把方法装饰成属性，可以直接调用
    def content_html(self):#直接渲染模板
        from blog.models import Post #避免循环引用
        from comment.models import Comment
        result=""
        if self.display_type==self.DISPLAY_HTML:
            result=self.content
        elif self.display_type==self.DISPLAY_LATEST:
            context={
                'posts':Post.latest_posts(with_related=False)[:10]
            }
            result=render_to_string('config/blocks/sidebar_posts.html',context)
        elif self.display_type==self.DISPLAY_HOT:
            context={
                'posts':Post.hot_posts()[:10]
            }
            result=render_to_string('config/blocks/sidebar_posts.html',context)
        elif self.display_type==self.DISPLAY_COMMENT:
            context={
                'comments':Comment.objects.filter(status=Comment.STATUS_NORMAL).order_by('-id')[:5],
            }
            result=render_to_string('config/blocks/sidebar_comments.html',context)
        return result
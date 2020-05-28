import xadmin
from xadmin.filters import RelatedFieldListFilter
from xadmin.filters import manager
from xadmin.layout import Row, Fieldset, Container
from django.urls import reverse
from django.utils.html import format_html
from .adminforms import PostAdminForm
from .models import Post, Category, Tag
from web2.BaseOwnerAdmin import BaseOwnerAdmin

class CategoryOwnerFilter(RelatedFieldListFilter):
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):  # 确认字段是否被当前的过滤器处理
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')  # 这个方法在父类中默认是查询所有数据

manager.register(CategoryOwnerFilter, take_priority=True)

# class PostInline:#关联文章和分类：在分类编辑页面可进行文章的增删改
#     form_layout=(#可选择继承admin.StackedInline,只是样式不一样
#         Container(
#             Row('title','desc'),
#         )
#     )
#     extra = 1#显示控制多少篇文章
#     model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    # inlines = [PostInline,]#关联
    list_display = ('name','status','is_nav','created_time','post_count')
    fields = ('name','status','is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ['title','category','status','created_time','owner','operator']
    list_display_links = []
    list_filter = ['category',]
    search_fields = ['title','category__name']
    actions_on_top = True
    actions_on_bottom = False
    save_on_top = True

    #编辑页面

    # fields = (#指定哪些字段显示和展示顺序
    #     'title',
    #     'category',
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    exclude = ('owner',)#指定哪些字段不显示

    form_layout =(
        Fieldset(
            '基础信息',
            Row('title','category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        )
    )
    # filter_horizontal = ('tag',)#控制多字段栈展示的配置
    # filter_vertical = ('tag',)

    def operator(self,obj):#自定义显示的字段
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change',args=(obj.id,))
        )
    operator.short_description = '操作'#表头的展示文案

    # def get_media(self):
        # # xadmin基于bootstrap，引入会页面样式冲突.
        # media = super().get_media()
        # media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
        # media.add_css({
            # 'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
        # })
        # return media

# @admin.register(LogEntry)
# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = ['object_repr','object_id','action_flag','user','change_message']
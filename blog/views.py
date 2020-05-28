# Create your views here.
from datetime import date

from django.core.cache import cache
from django.db.models import F, Q
from django.shortcuts import  get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Tag,Post,Category
from config.models import SideBar,Link
#文章列表function
# def post_list(request,category_id=None,tag_id=None):
#     tag=None
#     category=None
#
#     if tag_id:
#         try:
#             tag=Tag.objects.get(id=tag_id)
#         except Tag.DoesNotExist:
#             post_list=[]
#         else:
#             post_list=tag.post_set.filter(status=Post.STATUS_NORMAL)
#     else:
#         post_list=Post.objects.filter(status=Post.STATUS_NORMAL)
#         if category_id:
#             try:
#                 category=Category.objects.get(id=category_id)
#             except  Category.DoesNotExist:
#                 category=None
#             else:
#                 post_list=post_list.filter(category_id=category_id)
#     context={
#         'category':category,
#         'tag':tag,
#         'post_list':post_list,
#         'sidebars':SideBar.get_all()
#     }
#     context.update(Category.get_navs())
#     return render(request,'blog/list.html',context=context)
#文章内容function
# def post_detail(request,post_id):
#     try:
#         post=Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post=None
#     context={
#         'post': post,
#         'sidebars': SideBar.get_all()
#     }
#     context.update(Category.get_navs())
#     if post:
#         post.pv=F('pv')+1#原子性操作，防止多线程问题
#         post.save()
#     return render(request, 'blog/detail.html', context=context)
#友链
# def links(request):
#     return HttpResponse('LINKS')

class CommonView:#基础类：处理通用数据
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
            'sidebars':SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context

class IndexView(CommonView,ListView):#首页类
    queryset = Post.latest_posts()
    paginate_by = 6
    context_object_name = 'post_list'#在模板中使用,没有设置时，需要使用object_list变量
    template_name = 'blog/list.html'


class PostDetailView(CommonView,DetailView):#文章内容类
    queryset = Post.latest_posts()
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):#访问统计
        increase_pv=False
        increase_uv=False
        uid=self.request.uid
        pv_key='pv:%s:%s'%(uid,self.request.path)
        uv_key = 'pv:%s:%s:%s' % (uid, str(date.today()),self.request.path)
        if not cache.get(pv_key):#判断是否有缓存
            increase_pv=True
            cache.set(pv_key,1,1*60) #一分钟内有效
        if not cache.get(uv_key):
            increase_uv=True
            cache.set(uv_key,1,24*60*60) #一天内有效

        if increase_uv and increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1,uv=F('uv')+1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('uv') + 1)

    def get_context_data(self,**kwargs):#
        context = super().get_context_data(**kwargs)
        post_id=self.kwargs.get('post_id')
        post=get_object_or_404(Post,pk=post_id)

        next_post = Post.objects.filter(created_time__gt=post.created_time,category=post.category_id).last()# 指创建时间小于当前这篇文章的文章，指在这篇文章之后创建的文章
        previous_post = Post.objects.filter(created_time__lt=post.created_time,category=post.category_id).first()
        context.update({
            'next_post':next_post,
            'previous_post':previous_post,
        })
        return context

class CategoryView(IndexView):#分类列表页
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        category_id=self.kwargs.get('category_id')
        category=get_object_or_404(Category,pk=category_id)#获取一个对象的实例，如果没有抛出404
        context.update({
            'category':category,
        })
        return context

    def get_queryset(self):#重写queryset,根据分类过滤
        queryset=super().get_queryset()
        category_id=self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):#标签列表页
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        tag_id=self.kwargs.get('tag_id')
        tag=get_object_or_404(Tag,pk=tag_id)
        context.update({
            'tag':tag,
        })
        return context

    def get_queryset(self):
        queryset=super().get_queryset()
        tag_id=self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)

class SearchView(IndexView):#搜索列表页
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword':self.request.GET.get('keyword','')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword=self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword)|Q(desc__icontains=keyword))#联合查询
        #实现select * from post where title like '%<keyword>%' or desc like '%<keyword>%'


class AuthorView(IndexView):
    def get_queryset(self):
        queryset=super().get_queryset()
        author_id=self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)


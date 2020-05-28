from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from blog.models import Post, Category, Tag
from blog.serializers import (
    PostSerializer, PostDetailSerializer,
    CategorySerializer,
    CategoryDetailSerializer, TagSerializer, TagDetailSerializer)

# class PostViewSet(viewsets.ModelViewSet):
#     serializer_class = PostSerializer
#     queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    #permission_classes = [IsAdminUser] #写入时的权限校验，即POST(新建),PUT(修改),DELETE(删除)
    #GET为(查询)

class PostViewSet(viewsets.ReadOnlyModelViewSet):#当没有写入需求时，可以使用ReadOnlyModelViewSet
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class=PostDetailSerializer
        return super().retrieve(request,*args,**kwargs)

    def filter_queryset(self, queryset):
        category_id=self.request.query_params.get('category')
        if category_id:
            queryset=queryset.filter(category_id=category_id)
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class=CategoryDetailSerializer
        return super().retrieve(request,*args,**kwargs)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.filter(status=Tag.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class=TagDetailSerializer
        return super().retrieve(request,*args,**kwargs)
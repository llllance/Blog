from rest_framework import serializers, pagination

from .models import Post, Category, Tag


class PostSerializer(serializers.HyperlinkedModelSerializer):#用来序列化的类

    url=serializers.HyperlinkedIdentityField(view_name='api-post-detail')
    category=serializers.SlugRelatedField(#外键数据需要用SlugRelatedField
        read_only=True,
        slug_field='name'#指定展示的字段
    )
    tag=serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    owner=serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    created_time=serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model=Post
        fields=['url','id','title','category','tag','owner','created_time']

class PostDetailSerializer(PostSerializer):
    class Meta:
        model=Post
        fields=['id','title','category','tag','owner','content_html','created_time']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=(
            'id','name','created_time',
        )

class CategoryDetailSerializer(CategorySerializer):
    posts=serializers.SerializerMethodField('paginated_posts')#把posts字段获取的内容映射到paginated_posts方法里，即posts对应的数据通过paginated_posts来获取

    def paginated_posts(self,obj):
        posts=obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator=pagination.PageNumberPagination()
        page=paginator.paginate_queryset(posts,self.context['request'])
        serializer=PostSerializer(page,many=True,context={'request':self.context['request']})
        return {
            'count':posts.count(),
            'results':serializer.data,
            'previous':paginator.get_previous_link(),
            'next':paginator.get_next_link(),
        }
    class Meta:
        model=Category
        fields=(
            'id','name','created_time','posts'
        )

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields=(
            'id','name','created_time',
        )

class TagDetailSerializer(TagSerializer):
    posts=serializers.SerializerMethodField('paginated_posts')#把posts字段获取的内容映射到paginated_posts方法里，即posts对应的数据通过paginated_posts来获取

    def paginated_posts(self,obj):
        posts=obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator=pagination.PageNumberPagination()
        page=paginator.paginate_queryset(posts,self.context['request'])
        serializer=PostSerializer(page,many=True,context={'request':self.context['request']})
        return {
            'count':posts.count(),
            'results':serializer.data,
            'previous':paginator.get_previous_link(),
            'next':paginator.get_next_link(),
        }
    class Meta:
        model=Tag
        fields=(
            'id','name','created_time','posts'
        )
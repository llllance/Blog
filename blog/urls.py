from django.urls import path,re_path
from django.contrib.sitemaps import views as sitemap_views
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from blog.views import PostDetailView, IndexView, CategoryView, TagView, SearchView, AuthorView
from comment.views import CommentView
from config.views import LinkListView
from web2.autocomplete import CategoryAutocomplete,TagAutocomplete

urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('category/<int:category_id>/',CategoryView.as_view(),name='category-list'),
    path('tag/<int:tag_id>/',TagView.as_view(),name='tag-list'),
    path('post/<post_id>.html',PostDetailView.as_view(),name='post-detail'),
    path('search/',SearchView.as_view(),name='search'),
    path('author/<int:owner_id>',AuthorView.as_view(),name='author',),
    path('links/',LinkListView.as_view(),name='links'),
    path('comment/',CommentView.as_view(),name='comment'),
    re_path(r'^rss|feed/',LatestPostFeed(),name='rss'),
    re_path(r'^sitemap\.xml$',sitemap_views.sitemap,{'sitemaps':{'posts':PostSitemap}}),
    path('category-autocomplete/',CategoryAutocomplete.as_view(),name='category-autocomplete'),
    path('tag-autocomplete/',TagAutocomplete.as_view(),name='tag-autocomplete'),
]

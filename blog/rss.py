from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from .models import Post

class ExtendedRSSFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('content:html', item['content_html'])

class LatestPostFeed(Feed):
    feed_type = ExtendedRSSFeed#可以不写，默认是Rss201rev2Feed
    title='Hai Blog System'
    link='/rss/'
    description = 'blog system power by django'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]

    def item_title(self,item):#返回文章名
        return item.title

    def item_description(self, item):##返回文章的摘要
        return item.desc

    def item_link(self, item):#返回文章的URL
        return reverse('post-detail',args=[item.pk])

    def item_extra_kwargs(self, item):#返回文章内容
        return {'content_html':self.item_content_html(item)}

    def item_content_html(self,item):
        return item.content_html
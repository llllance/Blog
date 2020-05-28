"""web2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from blog.apis import PostViewSet, CategoryViewSet, TagViewSet
router=DefaultRouter()
router.register('post',PostViewSet,base_name='api-post')
router.register('category',CategoryViewSet,base_name='api-category')
router.register('tag',TagViewSet,base_name='api-tag')
urlpatterns = [
    path('admin/', xadmin.site.urls,name='xadmin'),
    path('',include('blog.urls')),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path('api/',include(router.urls)),
    path('api/docs/',include_docs_urls(title='web apis')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/',include(debug_toolbar.urls))
    ]+urlpatterns
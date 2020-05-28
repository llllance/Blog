from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView

from blog.views import CommonView

from .models import Link


class LinkListView(CommonView,ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'


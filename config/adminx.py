import xadmin
from django.contrib import admin
from .models import SideBar,Link
from web2.BaseOwnerAdmin import BaseOwnerAdmin
# Register your models here.

@xadmin.sites.register(SideBar)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title','display_type',
                    'content','created_time')

    fields = ('title','display_type','content')

    def save_model(self, request, obj, form, change):
        obj.owner=request.user
        return super(SideBarAdmin, self).save_model(request,obj,form,change)



@xadmin.sites.register(Link)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)
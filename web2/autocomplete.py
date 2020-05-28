from dal import autocomplete

from blog.models import Category,Tag

class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:#判断用户是否登陆,没登陆则返回空
            return Category.objects.none()

        qs=Category.objects.filter(owner=self.request.user)

        if self.q:#q是url参数上传递过来的值
            qs=qs.filter(name__istartswith=self.q)
        return qs


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:#is_authenitcate是属性不是方法，不可以加上括号
            return Tag.objects.none()

        qs = Tag.objects.filter(owner=self.request.user)

        if self.q:  # q是url参数上传递过来的值
            qs = qs.filter(name__istartswith=self.q)
        return qs

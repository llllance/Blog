from django import template
from comment.forms import CommentForm
from comment.models import Comment

register=template.Library()
#自定义标签，需要放在正确的位置，django会自动查找
@register.inclusion_tag('comment/block.html')
def comment_block(target):
    return {
        'target':target,
        'comment_form':CommentForm(),
        'comment_list':Comment.get_by_target(target),
    }
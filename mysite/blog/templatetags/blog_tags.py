from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    """
        Шаблонный тег, возвращающий количество опубликованных в блоге статей.
        После добавления этого модуля, необходима перезагрузка сервера разработки, для регистрации определённых тегов
        и фильтров.
    """
    return Post.published.count()


@register.inclusion_tag('post/latest_posts.html')
def show_latest_posts(count=5):
    """
        Инклюзивный тег, для добавления последних статей блога на боковую панель.
        С помощью него мы задействуем переменные контекста, возвращаемые тегом, для формирования шаблона.
    """
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    """
        Тег для отображения статей с наибольшим количеством комментариев.
        Результат его действий сохраняется в переменную, поэтому может быть использован многократно и без повторных
        вычислений.
    """
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    """
        Регистрация фильтра Markdown.
        Он необходим для того, чтобы добавить возможность заполнять тело статьи с помощью форматирования Markdown,
        которое будет формировать корректный HTML при отображении статьи.
    """
    return mark_safe(markdown.markdown(text))

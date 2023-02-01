# Вся логика приложения описывается здесь. Каждый обработчик получает HTTP-запрос, обрабатывает его и получает ответ.

from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    """
        Создаём обработчик post_list. Он получает объект request в качестве аргумента и является обязательным для всех
        обработчиков. В этой функции мы запрашиваем из базы данных все опубликованные статьи с помощью менеджера
        published.
        После этого мы используем функцию render() для формирования шаблона со списком статей. Она принимает объект
        запроса request, путь к шаблону и переменные контекста для этого шаблона. В ответ вернётся объект HttpResponse
        со сформированным текстом (обычно это HTML - код).
    """
    posts = Post.published.all()
    #  Импортируем классы-пагинаторы из Django, для постраничного отображения постов
    objects_list = Post.published.all()
    paginator = Paginator(objects_list, 3)  # Отображение по три поста на странице
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)  # Если страница не является целым числом - возвращаем первую страницу
    except EmptyPage:
        posts = paginator.page(
            paginator.num_pages)  # Если номер страницы больше общего количества страниц - возвращаем последнюю
    return render(request, 'post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    """
        Это обработчик страницы статьи. Он принимает на вход аргументы year, month, day и post для получения статьи по
        указанным слагу и дате. Обратите внимание на то, что когда мы создали модель Post, у неё был указа атрибут
        unique_for_date для поля slug.
        Таким образом мы добавили ограничение, чтобы слаг был уникальным для статей, созданных в один день. Поэтому
        гарантированно сможем получить статью по комбинации этих полей.
        В обработчике используется get_object_or_404(), для того, чтобы найти нужную статью. Эта функция возвращает
        объект, который подходит по указанным параметрам, или вызывает исключение HTTP404, если не найдёт ни одной
        статьи.
    """
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    return render(request, 'post/detail.html', {'post': post})

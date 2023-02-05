# Вся логика приложения описывается здесь. Каждый обработчик получает HTTP-запрос, обрабатывает его и получает ответ.
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


def post_share(request, post_id):
    """
        Обработчик для получения данных формы и отправки их на почту, при условии, что они корректны. Для отображения
        пустой формы и обработки введённых данных, используется один и тот же обработчик. Для разделения логики
        отображения формы или её обработки, используется запрос request. Список полей с ошибками смотрим в form.errors
    """
    post = get_object_or_404(Post, id=post_id, status='published')  # Получение статьи по идентификатору
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)  # Форма была отправлена на сохранение
        if form.is_valid():  # Все поля формы прошли валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) рекомендует вам прочитать "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:  # Отправка электронной почты
        form = EmailPostForm()
    return render(request, 'post/share.html', {'post': post, 'form': form, 'sent': sent})


def post_list(request):
    """
        Создаём обработчик post_list. Он получает объект request в качестве аргумента и является обязательным для всех
        обработчиков. В этой функции мы запрашиваем из базы данных все опубликованные статьи с помощью менеджера
        published.
        После этого мы используем функцию render() для формирования шаблона со списком статей. Она принимает объект
        запроса request, путь к шаблону и переменные контекста для этого шаблона. В ответ вернётся объект HttpResponse
        со сформированным текстом (обычно это HTML - код).
    """
    # posts = Post.published.all()
    #  Импортируем классы-пагинаторы из Django, для постраничного отображения постов
    objects_list = Post.published.all()
    paginator = Paginator(objects_list, 3)  # Отображение по три поста на странице
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)  # Если страница не является целым числом — возвращаем первую страницу
    except EmptyPage:
        posts = paginator.page(
            paginator.num_pages)  # Если номер страницы больше общего количества страниц — возвращаем последнюю
    return render(request, 'post/list.html', {'page': page, 'posts': posts})


# Постраничное отображение работает следующим образом:
# 1. Инициализируем объект класса Paginator, указав количество объектов на одной странице;
# 2. Извлекаем из запроса GET-параметр 'page', который указывает текущую страницу;
# 3. Получаем список объектов на нужной странице с помощью метода 'page()' класса Paginator;
# 4. Если указанный параметр 'page' не является целым числом, обращаемся к первой странице. Если 'page' больше, чем общее
# количество страниц — возвращаем последнюю;
# 5. Передаём номер страницы и полученные объекты в шаблон.


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
    # Дорабатываем обработчик страницы статьи, для отображения формы и сохранения комментариев
    comments = post.comments.filter(active=True)  # Список активных комментариев для этой статьи
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)  # Пользователь отправил комментарий
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)  # Создаём комментарий, но пока не сохраняем в базе данных
            new_comment.post = post  # Привязываем комментарий к текущей статье
            new_comment.save()  # Сохраняем комментарий в базе данных
    else:
        comment_form = CommentForm()
    return render(request, 'post/detail.html',
                  {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})

# Модели данных приложения. В любом Django-приложении должен быть этот файл, но он может оставаться пустым.
"""
    Модель - это Python-класс, который является наследником django.db.models.Model. Каждый атрибут представляет собой
    поле в базе данных. Django создаёт таблицу в базе данных для каждой модели, определённой в models.py. Когда мы
    создаём модель, Django предоставляет удобный ИНТЕРФЕЙС (Application Programming Interface - API) для формирования
    запросов в базу данных.
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Модель данных для статей блога.
class PublishedManager(models.Manager):
    """
        Метод менеджера get_queryset() возвращает QuerySet, который будет выполняться. Мы переопределяем его и добавляем
        фильтр над результирующим QuerySet'ом. Также мы описываем менеджер и добавляем его в модель Post. Теперь мы можем
        использовать его для выполнения запросов.
    """

    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Отложено'),
        ('published', 'Опубликовано'),
    )
    title = models.CharField(max_length=250)  # Поле заголовка статьи. Тип VARCHAR в базе данных
    slug = models.SlugField(max_length=250, unique_for_date='publish')  # Поле для формирования URL'ов
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')  # Внешний ключ, определяющий отношение "один ко многим"
    body = models.TextField()  # Основное содержание статьи, которое будет сохранено в столбце TEXT в SQL базе данных
    publish = models.DateTimeField(
        default=timezone.now)  # Поле даты, сохраняющее дату публикации статьи. Функция 'now' - по умолчанию, и возвращает текущие дату и время
    created = models.DateTimeField(
        auto_now_add=True)  # Это поле даты указывает, когда статья была создана. Параметр 'auto_now_add' - автосохранение при создании объекта
    update = models.DateTimeField(
        auto_now=True)  # Дата и время, указывающие на период, когда статья была отредактирована. Параметр 'auto_now' - указание даты на момент сохранения.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='draft')  # Поле отображения статуса статьи. Параметр CHOICES ограничивает возможные значения из указанного списка.
    objects = models.Manager()  # Менеджер по умолчанию
    published = PublishedManager()  # Новый менеджер

    class Meta:
        ordering = (
            '-publish',)  # Указали Django, порядок сортировки статей по умолчанию — по убыванию (префикс "-") даты публикации поля 'publish'.

    def __str__(self):  # Метод __str__() возвращает отображение объекта, понятное человеку
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

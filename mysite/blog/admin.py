# Здесь мы регистрируем модели для добавления их в систему администрирования Django.

from django.contrib import admin
from .models import Post, Comment


# Настройка отображения модели в админке (фильтр постов по времени, дате и статусу)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
        Модель для управления постами в админке.
    """
    list_display = ('title', 'slug', 'author', 'publish', 'status')  # Это наши отображаемые в списке статей поля
    list_filter = ('status', 'created', 'publish', 'author')  # Фильтр, сортирующий статьи по полям указанным выше
    search_fields = ('title', 'body')  # Строка поиска
    prepopulated_fields = {'slug': ('title',)}  # Этот атрибут генерирует SLUG автоматически
    raw_id_fields = ('author',)  # Поле для поиска автора (вместо выпадающего списка). Удобно когда сотни авторов
    date_hierarchy = 'publish'  # Атрибут, добавляющий ссылки для навигации по датам
    ordering = ('status', 'publish')  # Настройка сортировки, которая выше


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
        Модель для управления комментариями в админке.
    """
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

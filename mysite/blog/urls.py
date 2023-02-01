'''
    Определяем пространство имён приложения в переменной app_name. Это позволит нам сгруппировать адреса для приложения
    блога и использовать их названия для доступа к ним.
    Мы объявили два шаблона, используя функцию path(). Первый шаблон не принимает никаких аргументов, и сопоставляется
    с обработчиком post_list. Второй — вызывает функцию post_detail и принимает в качестве параметров: year, month, day
    и post.
    Если использование path() и конвертеров не подходит, можно задействовать re_path() - эта функция позволяет задавать
    шаблоны URL'ов в виде регулярных выражений
'''

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
]

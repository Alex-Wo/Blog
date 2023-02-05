from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    """
        Форма для отправки статьи на email, на основе встроенной в Django подсистемы форм. Класс формы, унаследованный
        от Form.
    """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    """
        Форма, позволяющая пользователям оставлять комментарии.
    """

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')  # Поля, доступные пользователям

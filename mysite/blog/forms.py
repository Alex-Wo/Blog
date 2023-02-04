from django import forms


# Форма для отправки статьи на email, на основе встроенной в Django подсистемы форм. Класс формы, унаследованный от Form.
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

from django import forms
from .models import *


class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advertisements
        widgets = {'title': forms.TextInput(attrs={'size': '100'})}
        fields = ('category', 'title', 'text', 'content', 'photo', )

    def __init__(self, *args, **kwargs):
        super(AdvertForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = 'Категория:'
        self.fields['title'].label = 'Заголовок:'
        self.fields['text'].label = 'Текст объявления:'
        self.fields['content'].label = 'Медиа:'
        self.fields['photo'].label = 'Фото'


class CommentFilterForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(CommentFilterForm, self).__init__(*args, **kwargs)
        self.fields['title'] = forms.ModelChoiceField(
            label='Фильтр',
            queryset=Advertisements.objects.filter(author_id=user.id).order_by('-created_at'),
            empty_label='Все',
            required=False,
            to_field_name='title'  # Добавляем аргумент to_field_name для выбора поля заголовка
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Переданное послание :"
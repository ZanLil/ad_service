from django import forms

from .models import Ad, Response


class MultipleFileInput(forms.ClearableFileInput):
    """Widget для input с возможностью выбрать более одного файла."""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class AdForm(forms.ModelForm):
    """Форма объявления."""
    media_files = MultipleFileField(label='Изображения и видео', widget=MultipleFileInput(attrs={
        'multiple': True,
        'class': 'form-control',
    }), required=False)
    header = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    body = forms.CharField(label='Содержание', widget=forms.Textarea(attrs={
        'class': 'form-control',
    }))
    category = forms.ChoiceField(label='Категория', choices=Ad.Category.choices, widget=forms.Select(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = Ad
        fields = ['header', 'body', 'category']


class SendResponseForm(forms.ModelForm):
    """Форма отклика."""
    text = forms.CharField(label='Текст', widget=forms.Textarea(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = Response
        fields = ['text']

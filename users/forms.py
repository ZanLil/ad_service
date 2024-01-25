from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from main.models import Ad
from users.models import User


class SignUpForm(UserCreationForm):
    """Форма регистрации пользователя."""
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    email = forms.EmailField(label='Адрес электронной почты', widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))
    password1 = forms.CharField(label='Пароль',
                                help_text='''<ul>
                                                <li>Пароль не должен быть слишком похож на другую вашу личную информацию.</li>
                                                <li>Ваш пароль должен содержать как минимум 8 символов.</li>
                                                <li>Пароль не должен быть слишком простым и распространенным.</li>
                                                <li>Пароль не может состоять только из цифр.</li>
                                            </ul>''',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                }))
    password2 = forms.CharField(label='Подтверждение пароля',
                                help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserAuthenticationForm(AuthenticationForm):
    """Форма входа."""
    username = forms.EmailField(label='Адрес электронной почты', widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))


class ConfirmationCodeForm(forms.Form):
    """Форма подтверждения кода."""
    confirmation_code = forms.CharField(label='Код подтверждения', max_length=6,
                                        help_text='На ваш электронный адрес был выслан код подтверждения',
                                        widget=forms.NumberInput(attrs={
                                            'class': 'form-control',
                                        }))


class ResponseFilterForm(forms.Form):
    """Форма фильтрации откликов."""
    ad = forms.ModelChoiceField(queryset=Ad.objects.none(), widget=forms.Select(attrs={
        'class': 'form-control'
    }), empty_label="All Ads", required=False)

    def __init__(self, user, *args, **kwargs):
        super(ResponseFilterForm, self).__init__(*args, **kwargs)
        self.fields['ad'].queryset = Ad.objects.filter(author=user)

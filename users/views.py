import random

from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

from main.forms import AdForm
from main.models import Ad, MediaFile, Response
from .forms import SignUpForm, UserAuthenticationForm, ConfirmationCodeForm, ResponseFilterForm
from .models import User


def register(request):
    """Функция-представление регистрации пользователя."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])

            confirmation_code = str(random.randint(100000, 999999))
            user.confirmation_code = confirmation_code
            user.save()

            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {confirmation_code}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return redirect('users:confirm_code')
    else:
        form = SignUpForm()
    return render(request, 'users/user/register.html', {'form': form})


def login_user(request):
    """Функция-представление входа пользователя."""
    if request.method == 'POST':
        form = UserAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user, backend='users.authentication.EmailAuthBackend')
                return redirect('main:index')
    else:
        form = UserAuthenticationForm()
    return render(request, 'users/user/login.html', {'form': form})


def logout_user(request):
    """Функция-представление выхода пользователя."""
    logout(request)
    return redirect('main:index')


def confirm_code(request):
    """Функция-представление подтверждения."""
    if request.method == 'POST':
        form = ConfirmationCodeForm(request.POST)
        if form.is_valid():
            confirmation_code = form.cleaned_data['confirmation_code']
            user = User.objects.filter(confirmation_code=confirmation_code).first()

            if user:
                user.confirmation_code = None
                user.save()
                login(request, user, backend='users.authentication.EmailAuthBackend')
                return redirect('main:index')

    else:
        form = ConfirmationCodeForm()

    return render(request, 'users/user/confirm_code.html', {'form': form})


@login_required
def my_ads(request):
    """Функция-представление объявлений созданных текущим пользователем."""
    ads = Ad.objects.filter(author=request.user)
    context = {'ads': ads}
    return render(request, 'users/my_ads.html', context)


@login_required
def my_ad_detail(request, ad_id):
    """Функция-представление объявления созданного текущим пользователем."""
    ad = get_object_or_404(Ad, author=request.user, pk=ad_id)
    context = {'ad': ad}
    return render(request, 'users/my_ad_detail.html', context)


@login_required
def edit_ad(request, ad_id):
    """Функция-представление редактирования объявления, созданного текущим пользователем."""
    ad = get_object_or_404(Ad, author=request.user, pk=ad_id)
    if request.method == 'POST':
        form = AdForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            ad.header = cd['header']
            ad.category = cd['category']
            ad.body = cd['body']
            ad.save()
            if request.FILES.getlist('media_files'):
                for file in MediaFile.objects.filter(ad=ad):
                    file.delete()
                for file in request.FILES.getlist('media_files'):
                    MediaFile.objects.create(ad=ad, file=file)
            return redirect('users:my_ad_detail', ad_id=ad.id)
    else:
        form = AdForm(instance=ad)
    context = {'form': form, 'ad': ad}
    return render(request, 'users/edit_ad.html', context)


@login_required
def my_responses(request):
    """Функция-представление откликов, которые сделал текущий пользователь."""
    responses = Response.objects.filter(user=request.user)
    context = {'responses': responses}
    return render(request, 'users/my_responses.html', context)


@login_required
def responses_on_my_ads(request):
    """Функция-представление откликов на объявления созданные текущим пользователем."""
    current_user = request.user
    ads = Ad.objects.filter(author=current_user)
    user_responses = Response.objects.filter(ad__in=ads, ad__executor=None)
    form = ResponseFilterForm(user=current_user, data=request.GET)
    selected_ad = form['ad'].value()

    if selected_ad:
        user_responses = user_responses.filter(ad=selected_ad)
    context = {'responses': user_responses, 'form': form, 'selected_ad': selected_ad}
    return render(request, 'users/responses_on_my_ads.html', context)


@login_required
def delete_response(request, ad_id):
    """Функция-представление удаления объявления, созданного текущим пользователем."""
    ad = Ad.objects.get(pk=ad_id)
    ad.delete()
    return redirect('users:responses_on_my_ads')


@login_required
def accept_response(request, ad_id):
    """Функция-представление принятия отклика на созданное текущим пользователем объявление."""
    ad = Ad.objects.get(pk=ad_id)
    ad.executor = request.user
    ad.save()
    send_mail(
        'Ваш отклик был принят',
        f'Ваш отклик на объявлении "{ad.header}" был принят',
        settings.DEFAULT_FROM_EMAIL,
        [ad.executor.email],
        fail_silently=True,
    )
    return redirect('users:responses_on_my_ads')

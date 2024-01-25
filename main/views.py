from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import AdForm, SendResponseForm
from .models import Ad, MediaFile


@login_required
def index(request):
    """Функция-представление главной страницы."""
    ads = Ad.objects.exclude(author=request.user)
    context = {'ads': ads}
    return render(request, 'main/index.html', context)


@login_required
def create_ad(request):
    """Функция-представление создания объявления."""
    if request.method == 'POST':
        ad_form = AdForm(request.POST)

        if ad_form.is_valid():
            ad = ad_form.save(commit=False)
            ad.author = request.user
            ad.save()
            for file in request.FILES.getlist('media_files'):
                MediaFile.objects.create(ad=ad, file=file)
            return redirect('users:my_ads')

    else:
        ad_form = AdForm()

    return render(request, 'main/ad/create.html', {'ad_form': ad_form})


@login_required
def detail_ad(request, ad_id):
    """Функция-представление детальной информации об объявлении."""
    ad = Ad.objects.get(pk=ad_id)
    is_response_sent = ad.responses.filter(user=request.user)
    context = {'ad': ad, 'is_response_sent': is_response_sent}
    return render(request, 'main/ad/detail.html', context)


@login_required
def send_response(request, ad_id):
    """Функция-представление отправки отклика на объявление."""
    if request.method == 'POST':
        form = SendResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            ad = Ad.objects.get(pk=ad_id)
            response.ad = ad
            if ad.responses.filter(user=response.user):
                raise Http404()
            response.save()
            send_mail(
                subject='На ваше объявление кто-то откликнулся',
                message=f'На ваше объявление "{response.ad.header}" откликнулся пользователь {response.user.username}\n\nДля более детальной информации перейдите в ваши отклики.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[response.user.email],
                fail_silently=True,
            )
            return redirect('main:detail_ad', ad_id=ad_id)
    else:
        form = SendResponseForm()
    context = {'form': form}
    return render(request, 'main/ad/send_response.html', context)

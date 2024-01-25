from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:ad_id>/', views.detail_ad, name='detail_ad'),
    path('<int:ad_id>/send_response/', views.send_response, name='send_response'),
    path('create_ad/', views.create_ad, name='create_ad'),
]

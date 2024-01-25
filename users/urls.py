from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/confirm_code/', views.confirm_code, name='confirm_code'),
    path('my_ads/', views.my_ads, name='my_ads'),
    path('my_ads/<int:ad_id>/', views.my_ad_detail, name='my_ad_detail'),
    path('my_ads/<int:ad_id>/edit_ad/', views.edit_ad, name='edit_ad'),
    path('my_responses/', views.my_responses, name='my_responses'),
    path('responses_on_my_ads/', views.responses_on_my_ads, name='responses_on_my_ads'),
    path('responses_on_my_ads/delete/<int:ad_id>/', views.delete_response, name='delete_response'),
    path('responses_on_my_ads/accept/<int:ad_id>/', views.accept_response, name='accept_response'),
    path('newsletter/', views.newsletter, name='newsletter'),
]

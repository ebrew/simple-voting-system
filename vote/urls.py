from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name="home"),
    path('account/login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('position2/', views.position2, name='position2'),
    path('position3/', views.position3, name='position3'),
    path('position4/', views.position4, name='position4'),
    path('position5/', views.position5, name='position5'),
    path('summary/', views.summary, name='summary'),
    path('voting/result/options/', views.options, name='options'),
    path('voting/result/overview/', views.overview, name='overview'),
    path('voting/result/final/', views.final_result, name='final'),
    path('vote/<str:cid>/<str:pid>', views.vote, name='vote'),
    path('users', views.users, name='users'),
    path('remove_user/<str:pk>', views.remove_user, name='remove'),
]

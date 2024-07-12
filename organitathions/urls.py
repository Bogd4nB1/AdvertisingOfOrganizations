from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('org/<int:pk>/', detail, name='detail'),
    path('tags/<str:slug>/', tag, name='tag'),
    path('search/', search_task, name='search'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('add_org/', add_org, name='add_org'),
    path('comment/<int:pk>', add_comment, name='comment'), # добавить коммент потом
    path('edit_org/', edit_org, name='edit_org'),
    path('delete_comment/', delete_comment, name='delete_comment'),
]
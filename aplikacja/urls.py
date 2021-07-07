from django.urls import path

from . import views
from .views import *

urlpatterns = [
    # ex: /aplikacja/
    path('', views.index, name='index'),
    path('post/ajax/add_dir_ajax/', views.add_dir_ajax, name='add_dir_ajax'),
    path('post/ajax/add_file_ajax/', views.add_file_ajax, name='add_file_ajax'),
    path('post/ajax/delete_dir/', views.delete_dir_ajax, name='delete_dir_ajax'),
    path('post/ajax/delete_file/', views.delete_file_ajax, name='delete_file_ajax'),
    # ex: /aplikacja/detail/file.name/
    path('detail/<str:name>/', views.detail, name='detail'),
    path('get/ajax/file/', views.select_file, name='select_file'),
    path('get/ajax/fileTree/', views.get_fileTree, name='get_fileTree'),
    path('post/ajax/rerun_frama/', views.rerun_frama_ajax, name='rerun_frama_ajax'),
    # ex: /aplikacja/change_prover/
    path('change_prover/', views.change_prover, name='change_prover'),
    # ex: /aplikacja/change_VC/
    path('change_VC/', views.change_VC, name='change_VC'),
    # ex: /aplikacja/login/
    path('login/', UserLogin.as_view(), name='login'),
    # ex: /aplikacja/authentication/
    path('authentication/', views.authentication, name='authentication'),
]

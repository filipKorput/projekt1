from django.urls import path

from . import views
from .views import *

urlpatterns = [
    # ex: /aplikacja/
    path('', views.index, name='index'),
    # ex: /aplikacja/add_dir/
    path('add_dir/', views.add_dir, name='add_dir'),
    path('post/ajax/add_dir_ajax/', views.add_dir_ajax, name='add_dir_ajax'),
    # ex: /aplikacja/add_file/
    path('add_file/', views.add_file, name='add_file'),
    path('post/ajax/add_file_ajax/', views.add_file_ajax, name='add_file_ajax'),
    # ex: /aplikacja/delete_dir/
    path('delete_dir/', views.delete_dir, name='delete_dir'),
    path('post/ajax/delete_dir/', views.delete_dir_ajax, name='delete_dir_ajax'),
    # ex: /aplikacja/delete_file/
    path('delete_file/', views.delete_file, name='delete_file'),
    path('post/ajax/delete_file/', views.delete_file_ajax, name='delete_file_ajax'),
    # ex: /aplikacja/detail/file.name/
    path('detail/<str:name>/', views.detail, name='detail'),
    path('get/ajax/file/', views.select_file, name='select_file'),
    path('get/ajax/fileTree/', views.get_fileTree, name='get_fileTree'),
    # ex: /aplikacja/rerun_frama/file.name/
    path('rerun_frama/<str:name>/', views.rerun_frama, name='rerun_frama'),
    path('post/ajax/rerun_frama/', views.rerun_frama_ajax, name='rerun_frama_ajax'),
    # ex: /aplikacja/change_prover/file.name/
    path('change_prover/<str:name>/', views.change_prover, name='change_prover'),
    # ex: /aplikacja/change_VC/file.name/
    path('change_VC/<str:name>/', views.change_VC, name='change_VC'),
    # ex: /aplikacja/login/
    path('login/', UserLogin.as_view(), name='login'),
    # ex: /aplikacja/authentication/
    path('authentication/', views.authentication, name='authentication'),
]

from django.urls import path

from . import views
from .views import *

urlpatterns = [
    # ex: /aplikacja/
    path('', views.index, name='index'),
    # ex: /aplikacja/add_dir/
    # path('add_dir/', views.add_dir, name='add_dir'),
    # ex:
    path('post/ajax/add_dir/', views.add_dir_ajax, name='add_dir'),
    # ex: /aplikacja/add_file/
    path('add_file/', views.add_file, name='add_file'),
    # ex: /aplikacja/delete_dir/
    path('delete_dir/', views.delete_dir, name='delete_dir'),
    # ex: /aplikacja/delete_file/
    path('delete_file/', views.delete_file, name='delete_file'),
    # ex: /aplikacja/detail/file.name/
    # path('detail/<str:name>/', views.detail, name='detail'),
    path('get/ajax/file/', views.get_file, name='select_file'),
    path('get/ajax/filesystem_tree/', views.get_filesystem_tree, name='get_filesystem_tree'),
    # ex: /aplikacja/rerun_frama/file.name/
    path('rerun_frama/<str:name>/', views.rerun_frama, name='rerun_frama'),
    # ex: /aplikacja/change_prover/file.name/
    path('change_prover/<str:name>/', views.change_prover, name='change_prover'),
    # ex: /aplikacja/change_VC/file.name/
    path('change_VC/<str:name>/', views.change_VC, name='change_VC'),
    # ex: /aplikacja/login/
    path('login/', UserLogin.as_view(), name='login'),
    # ex: /aplikacja/authentication/
    path('authentication/', views.authentication, name='authentication'),
]

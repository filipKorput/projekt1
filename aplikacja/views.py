from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render

from .models import Directory, User, File
from .forms import DirectoryForm, FileForm, ProversForm, VCsForm
from .obslugaFramy import *

import logging
from django.utils import timezone


authentication_json_error = JsonResponse({"error": "not_authenticated"}, status=401)


class UserLogin(LoginView):
    template_name = 'aplikacja/login.html'


def authentication(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    print(username + " " + password)
    print(user)

    if user is not None:
        login(request, user)
        print("zalogowano: " + username)
        return HttpResponseRedirect('..')
    return render(request, 'aplikacja/login.html')


def index(request):
    context = {
        'directory_list': Directory.objects.filter(availability=True, owner=request.user),
        'file_list': File.objects.filter(availability=True, owner=request.user)
    }
    return render(request, 'aplikacja/index.html', context)

logger = logging.getLogger(__name__)

def detail(request, name):
    file = File.objects.get(pk=name)
    logger.error(file)
    with open(file.blob.path, 'r', encoding='UTF-8') as fileObject:
        data = fileObject.read().replace('\n', '</br>')
    summary = file.summary.replace('\n', '<br>')
    sectionList = getSectionsOfFile(file)
    context = {
        'directory_list': Directory.objects.filter(availability=True, owner=request.user),
        'file_list': File.objects.filter(availability=True, owner=request.user),
        'file': file,
        'fileContent': data,
        'sectionList': sectionList,
        'proverForm': ProversForm(),
        'VCForm': VCsForm(),
        'summary': summary
    }
    return render(request, 'aplikacja/index.html', context)

def get_file(request):
    if not request.user.is_authenticated:
        return authentication_json_error

    if request.is_ajax and request.method == 'GET':
        file_pk = request.GET.get('file')

        if file_pk is None or not file_pk.isnumeric():
            return JsonResponse({"error": ""}, status=404)

        file = File.objects.get(pk=file_pk)

        if file is None or not file.available or file.owner != request.user:
            return JsonResponse({"error": ""}, status=404)


        file_sections = getSectionsOfFile(file)

        return JsonResponse(file_sections, status=200)

    return JsonResponse({"error": ""}, status=400)


def get_filesystem_tree(request):
    if not request.user.is_authenticated:
        return authentication_json_error

    if request.is_ajax and request.method == 'GET':
        entities = []

        for file in File.objects.all():
            if file.available and file.owner == request.user:
                entities.append({
                    "id": "fil" + str(file.pk),
                    "parent": "#" if file.parent_directory_id is None else "dir" + str(file.parent_directory.pk),
                    "text": file.name,
                })

        for directory in Directory.objects.all():
            if directory.available and directory.owner == request.user:
                entities.append({
                    "id": "dir" + str(directory.pk),
                    "parent": "#" if directory.parent_directory_id is None else "dir" + str(directory.parent_directory.pk),
                    "text": directory.name,
                })

        print(entities)

        return JsonResponse(entities, status=200, content_type="application/json", safe=False)

    return JsonResponse({"error": ""}, status=400)


def add_dir(request):
    form = DirectoryForm(request.POST)
    form.instance.creation_date = timezone.now()
    form.instance.availability = True
    form.instance.owner = request.user
    if form.is_valid():
        form.instance.save()
        return HttpResponseRedirect('..')
    return render(request, 'aplikacja/add_dir.html', {'form': form})

def add_dir_ajax(request):
    if not request.user.is_authenticated:
        return authentication_json_error

    if request.is_ajax and request.method == "POST":
        name = request.POST.get('directory_name')
        parent_dir_pk = request.POST.get('parent_dir_pk')
        user = request.user
        parent_directory = Directory.objects.filter(name=parent_dir_pk).first() if parent_dir_pk != "#" else None

        if parent_directory.owner != user:
            return JsonResponse({"error": ""}, status=400)

        if name is not None and user is not None:
            directory = Directory.create(name=name,
                                         description=None,
                                         owner=user,
                                         parent=parent_directory,
                                         availability=True,
                                         creation_date=timezone.now())
            directory.save()
            return JsonResponse({"instance": ""}, status=200)

    return JsonResponse({"error": ""}, status=400)



def add_file(request):
    form = FileForm(request.POST, request.FILES)
    form.instance.creation_date = timezone.now()
    form.instance.availability = True
    form.instance.owner = request.user
    if form.is_valid():
        form.instance.blob = request.FILES['blob']
        form.instance.save()
        file = File.objects.get(name=form.instance.name)
        prover = None
        VCs = []
        addSectionsOfFile(file, prover, VCs)
        return HttpResponseRedirect('..')
    return render(request, 'aplikacja/add_file.html', {'form': form})

def delete_dir(request):
    context = {
        'directory_list': Directory.objects.filter(availability=True),
    }
    if request.POST.get("name"):
        name = request.POST.get("name")
        d = Directory.objects.get(name=name)
        d.availability = False
        d.save()
        return HttpResponseRedirect('..')
    return render(request, 'aplikacja/delete_dir.html', context)

def delete_file(request):
    context = {
        'file_list': File.objects.filter(availability=True),
    }
    if request.POST.get("name"):
        name = request.POST.get("name")
        f = File.objects.get(name=name)
        f.availability = False
        f.save()
        return HttpResponseRedirect('..')
    return render(request, 'aplikacja/delete_file.html', context)


def rerun_frama(request, name):
    file = File.objects.get(name=name)
    prover = request.session.get('prover', '')
    VCs = request.session.get('VCs', [])
    updateFramaOfFile(file, prover, VCs)
    return HttpResponseRedirect('/aplikacja/detail/' + name)

def change_prover(request, name):
    prover = request.POST['prover']
    request.session['prover'] = prover
    print('Wybrano prover: ' + request.session['prover'])
    return HttpResponseRedirect('/aplikacja/detail/' + name + '/')

def change_VC(request, name):
    VCs = dict(request.POST).get('conditions', [])
    request.session['VCs'] = VCs
    print('Wybrano verification conditions:')
    print(request.session['VCs'])
    return HttpResponseRedirect('/aplikacja/detail/' + name + '/')


from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.core import serializers
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
        'file_list': File.objects.filter(availability=True, owner=request.user),
        'directoryForm': DirectoryForm(),
        'fileForm': FileForm(),
        'proverForm': ProversForm(),
        'VCForm': VCsForm()
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
        'summary': summary,
        'directoryForm': DirectoryForm(),
        'fileForm': FileForm()
    }
    return render(request, 'aplikacja/index.html', context)


def select_file(request):
    if not request.user.is_authenticated:
        return authentication_json_error

    if request.is_ajax and request.method == 'POST':
        file_name = request.POST.get('fileName')

        print(file_name)
        if file_name is None:
            print("no file")
            return JsonResponse({"error": ""}, status=404)

        file = File.objects.get(name=file_name)

        if file is None or not file.availability or file.owner != request.user:
            return JsonResponse({"error": ""}, status=404)

        with open(file.blob.path, 'r', encoding='UTF-8') as fileObject:
            data = fileObject.read().replace('\n', '</br>')
        summary = file.summary.replace('\n', '<br>')
        sectionList = getSectionsOfFile(file)

        directory = {
            'fileContent': data,
            'sectionList': sectionList,
            'summary': summary,
            'title': file.name
        }
        print("Still here")
        return JsonResponse(directory, status=200)

    return JsonResponse({"error": ""}, status=400)


def get_fileTree(request):
    if not request.user.is_authenticated:
        return authentication_json_error

    if request.is_ajax and request.method == 'GET':
        entities = []

        for file in File.objects.all():
            if file.availability and file.owner == request.user:
                entities.append({
                    "id": "fil" + str(file.name),
                    "parent": "dir" + str(file.parent.name),
                    "text": file.name,
                })

        for directory in Directory.objects.all():
            if directory.availability and directory.owner == request.user:
                entities.append({
                    "id": "dir" + str(directory.name),
                    "parent": "#" if directory.parent is None else "dir" + str(directory.parent.name),
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
        form = DirectoryForm(request.POST)
        form.instance.creation_date = timezone.now()
        form.instance.availability = True
        form.instance.owner = request.user
        if form.is_valid():
            form.instance.save()
            instance = form.save()
            ser_instance = serializers.serialize('json', [instance, ])
            return JsonResponse({"instance": ser_instance}, status=200)

    return JsonResponse({"error": "form.errors"}, status=400)


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


def add_file_ajax(request):
    if not request.user.is_authenticated:
        return authentication_json_error

    if request.is_ajax and request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        form.instance.creation_date = timezone.now()
        form.instance.availability = True
        form.instance.owner = request.user
        form.instance.blob = request.FILES.get("uploadedFile")
        print(form.instance.blob)
        print(form.errors)
        if form.is_valid():
            form.instance.save()
            instance = form.save()
            file = File.objects.get(name=form.instance.name)
            prover = None
            VCs = []
            addSectionsOfFile(file, prover, VCs)
            ser_instance = serializers.serialize('json', [instance, ])
            return JsonResponse({"instance": ser_instance}, status=200)
    return JsonResponse({"error": "form.errors"}, status=400)


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


def delete_dir_ajax(request):
    if not request.user.is_authenticated:
        return authentication_json_error

    if request.is_ajax and request.method == "POST":
        name = request.POST.get('name')
        d = Directory.objects.get(name=name)
        d.availability = False
        d.save()
        return JsonResponse({}, status=200)
    return JsonResponse({"error": "form.errors"}, status=400)


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


def delete_file_ajax(request):
    if not request.user.is_authenticated:
        return authentication_json_error

    if request.is_ajax and request.method == "POST":
        name = request.POST.get('name')
        f = File.objects.get(name=name)
        f.availability = False
        f.save()
        return JsonResponse({}, status=200)
    return JsonResponse({"error": "form.errors"}, status=400)


def rerun_frama(request, name):
    file = File.objects.get(name=name)
    prover = request.session.get('prover', '')
    VCs = request.session.get('VCs', [])
    updateFramaOfFile(file, prover, VCs)
    return HttpResponseRedirect('/aplikacja/detail/' + name)


def rerun_frama_ajax(request):
    if not request.user.is_authenticated:
        return authentication_json_error

    if request.is_ajax and request.method == 'POST':
        file_name = request.POST.get('fileName')

        print(file_name)
        if file_name is None:
            print("no file")
            return JsonResponse({"error": ""}, status=404)

        file = File.objects.get(name=file_name)

        if file is None or not file.availability or file.owner != request.user:
            return JsonResponse({"error": ""}, status=404)

        prover = request.session.get('prover', '')
        VCs = request.session.get('VCs', [])
        updateFramaOfFile(file, prover, VCs)

        with open(file.blob.path, 'r', encoding='UTF-8') as fileObject:
            data = fileObject.read().replace('\n', '</br>')
        summary = file.summary.replace('\n', '<br>')
        sectionList = getSectionsOfFile(file)

        directory = {
            'fileContent': data,
            'sectionList': sectionList,
            'summary': summary,
            'title': file.name
        }
        print("Still here")
        return JsonResponse(directory, status=200)

    return JsonResponse({"error": ""}, status=400)


def change_prover(request):
    prover = request.POST['prover']
    request.session['prover'] = prover
    print('Wybrano prover: ' + request.session['prover'])
    return HttpResponseRedirect('/aplikacja/')

def change_VC(request):
    VCs = dict(request.POST).get('conditions', [])
    request.session['VCs'] = VCs
    print('Wybrano verification conditions:')
    print(request.session['VCs'])
    return HttpResponseRedirect('/aplikacja/')


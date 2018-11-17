from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from tablib import Dataset
from .models import Part

def index(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            context = {
                'parts': Part.objects.all(),
            }
            return render(request, 'index.html', context)
        return render(request, 'login.html', {})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
    return redirect('/')

def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect('/')

def simple_upload(request):
    if request.method == 'POST':
        person_resource = PersonResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(
            dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(
                dataset, dry_run=False)  # Actually import now

    return render(request, 'core/simple_upload.html')

@login_required
def search(request):
    if request.method == 'GET':
        context = {}
        q = request.GET.get('q')
        if q:
            context.update({
                'q': q,
            })
            try:
                parts = Part.objects.filter(Q(partno__icontains=q) |
                                            Q(shelf__icontains=q) |
                                            Q(group__icontains=q) |
                                            Q(description__icontains=q))
                context.update({
                    'parts': parts,
                })
            except Part.DoesNotExist:
                pass
            return render(request, 'index.html', context)
        return redirect('/')

@login_required
@transaction.atomic
def new(request):
    if request.method == 'POST':
        partno = request.POST.get('partno')
        if partno:
            try:
                part, created = Part.objects.get_or_create(partno=partno)
                if created:
                    if request.POST.get('plus'):
                        part.update()
                        part.total = 1
                        part.save()
            except Part.DoesNotExist:
                pass
        context = {
            'parts': Part.objects.all(),
        }
        return render(request, 'index.html', context)

@login_required
@transaction.atomic
def plus(request):
    if request.method == 'POST':
        partno = request.POST.get('partno')
        if partno:
            try:
                part = Part.objects.get(partno=partno)
                part.plus()
                part.update()
                part.save()
            except Part.DoesNotExist:
                pass
        context = {
            'parts': Part.objects.all(),
        }
        return render(request, 'index.html', context)

@login_required
@transaction.atomic
def minus(request):
    if request.method == 'POST':
        partno = request.POST.get('partno')
        if partno:
            try:
                part = Part.objects.get(partno=partno)
                part.minus()
                part.update()
                part.save()
            except Part.DoesNotExist:
                pass
        context = {
            'parts': Part.objects.all(),
        }
        return render(request, 'index.html', context)

@login_required
@transaction.atomic
def edit(request):
    if request.method == 'POST':
        partno = request.POST.get('partno')
        new_partno = request.POST.get('new_partno')
        if partno:
            try:
                part = Part.objects.get(partno=partno)
                part.partno = new_partno
                part.save()
            except Part.DoesNotExist:
                pass
        context = {
            'parts': Part.objects.all(),
        }
        return render(request, 'index.html', context)

@login_required
@transaction.atomic
def delete(request):
    if request.method == 'POST':
        partno = request.POST.get('partno')
        if partno:
            try:
                part = Part.objects.get(partno=partno)
                part.delete()
            except Part.DoesNotExist:
                pass
        context = {
            'parts': Part.objects.all(),
        }
        return render(request, 'index.html', context)
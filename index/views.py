from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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


@login_required
def search(request):
    if request.method == 'GET':
        partno = request.GET.get('partno')
        if partno:
            context = {
                'partno': partno,
            }
            try:
                part = Part.objects.get(partno=partno)
                context.update({
                    'part': part,
                })
            except Part.DoesNotExist:
                pass
            if request.is_ajax():
                return render(request, 'search.html', context)
            return render(request, 'index.html', context)
        return redirect('/')

def list_view(request):
    if request.method == 'GET':
        context = {
            'parts': Part.objects.all(),
        }
        return render(request, 'list.html', context)

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
                context = {
                    'parts': Part.objects.all(),
                }
                return render(request, 'search.html', context)
            except Part.DoesNotExist:
                pass
        return redirect('/')

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
                context = {
                    'parts': Part.objects.all(),
                }
                return render(request, 'list.html', context)
            except Part.DoesNotExist:
                pass
        return redirect('/')

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
                context = {
                    'parts': Part.objects.all(),
                }
                return render(request, 'list.html', context)
            except Part.DoesNotExist:
                pass
        return redirect('/')

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
                context = {
                    'parts': Part.objects.all(),
                }
                return render(request, 'list.html', context)
            except Part.DoesNotExist:
                pass
        return redirect('/')

@login_required
@transaction.atomic
def delete(request):
    if request.method == 'POST':
        partno = request.POST.get('partno')
        if partno:
            try:
                part = Part.objects.get(partno=partno)
                part.delete()
                context = {
                    'parts': Part.objects.all(),
                }
                return render(request, 'list.html', context)
            except Part.DoesNotExist:
                pass
        return redirect('/')

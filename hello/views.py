from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Part

def index(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            context = {
                'parts': Part.objects.all(),
            }
            return render(request, 'list.html', context)
        return render(request, 'index.html', {})

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
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
            except Part.DoesNotExist:
                pass
        return redirect('/')

@login_required
@transaction.atomic
def minus(request):
    if request.method == 'POST':
        partno = request.POST.get('partno')
        print(partno)
        if partno:
            try:
                part = Part.objects.get(partno=partno)
                part.minus()
                part.update()
                part.save()
            except Part.DoesNotExist:
                pass
        return redirect('/')

@login_required
@transaction.atomic
def edit(request):
    if request.method == 'POST':
        partno = request.POST.get('partno')
        if partno:
            try:
                part = Part.objects.get(partno=partno)
                part.update()
                part.save()
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
            except Part.DoesNotExist:
                pass
        return redirect('/')

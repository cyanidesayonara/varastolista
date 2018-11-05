from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
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

@login_required
@transaction.atomic
def new(request):
    if request.method == 'POST':
        partno = request.POST.get('partno')
        part, created = Part.objects.get_or_create(partno=partno)
        if created:
            if request.POST.get('plus'):
                part.update()
                part.total = 1
                part.save()
        return redirect('/')

@login_required
@transaction.atomic
def plus(request):
    if request.method == 'POST':
        partno = request.POST.get('partno')
        part = Part.objects.get(partno=partno)
        if part:
            part.plus()
            part.update()
            part.save()
        return redirect('/')

@login_required
@transaction.atomic
def minus(request):
    if request.method == 'POST':
        partno = request.POST.get('partno')
        part = Part.objects.get(partno=partno)
        if part:
            part.minus()
            part.update()
            part.save()
        return redirect('/')

@login_required
@transaction.atomic
def edit(request):
    if request.method == 'POST':
        partno = request.POST.get('partno')
        part = Part.objects.get(partno=partno)
        print(part)
        if part:
            part.update()
            part.save()
        return redirect('/')

@login_required
@transaction.atomic
def delete(request):
    if request.method == 'POST':
        partno = request.POST.get('partno')
        part = Part.objects.get(partno=partno)
        if part:
            part.delete()
        return redirect('/')

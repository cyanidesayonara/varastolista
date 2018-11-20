from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Part
from .forms import PartForm

def index(request):
    if request.method == 'GET':
        user = request.user
        context = {}
        if user.is_authenticated:
            context.update({
                'parts': Part.objects.all(),
            })
        return render(request, 'index.html', context)

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
        partno = request.POST.get('orig_partno')
        if partno:
            try:
                part = Part.objects.get(partno=partno)
                form = PartForm(request.POST, instance=part)
                if form.is_valid():
                    form.save()
            except Part.DoesNotExist:
                pass
        else:
            # TODO
            print("no bueno")
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

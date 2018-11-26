from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Part
from .forms import PartForm

def index(request):
    if request.method == "GET":
        template = "index.html"
        context = {}
        user = request.user
        if user.is_authenticated:
            context.update({
                "parts": Part.objects.all(),
            })
        return render(request, template, context)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
    return redirect("/")

def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("/")

@login_required
def search(request):
    if request.method == "GET":
        template = "index.html"
        context = {}
        q = request.GET.get("q")
        if (q):
            context.update({
                "q": q,
                "parts": Part.search(q),
            })
        else:
            context.update({
                "parts": Part.objects.all(),
            })
        return render(request, template, context)

@login_required
def new(request):
    if request.method == "POST":
        template = "index.html"
        context = {}
        form = PartForm(request.POST)
        if form.is_valid():
            part, created = Part.objects.get_or_create(**form.cleaned_data)
            context.update({
                "mod_part": part,
                "message": "Added",
            })
        else:
            context.update({
                "errors": form.errors.items(),
            })
        context.update({
            "parts": Part.objects.all(),
        })
        return render(request, template, context)

@login_required
def plus(request):
    if request.method == "POST":
        template = "index.html"
        context = {}
        partno = request.POST.get("partno")
        if partno:
            try:
                part = Part.objects.get(partno=partno)
                part.plus()
                part.save()
                context.update({
                    "message": "+1",
                    "mod_part": part,
                })
            except Part.DoesNotExist:
                pass
        q = request.POST.get("q")
        if (q):
            context.update({
                "q": q,
                "parts": Part.search(q),
            })
        else:
            context.update({
                "parts": Part.objects.all(),
            })
        return render(request, template, context)

@login_required
def minus(request):
    if request.method == "POST":
        template = "index.html"
        context = {}
        partno = request.POST.get("partno")
        if partno:
            try:
                part = Part.objects.get(partno=partno)
                part.minus()
                part.save()
                context.update({
                    "message": "-1",
                    "mod_part": part,
                })
            except Part.DoesNotExist:
                pass
        q = request.POST.get("q")
        if (q):
            context.update({
                "q": q,
                "parts": Part.search(q),
            })
        else:
            context.update({
                "parts": Part.objects.all(),
            })
        return render(request, template, context)

@login_required
def edit(request):
    if request.method == "POST":
        template = "index.html"
        context = {}
        partno = request.POST.get("orig_partno")
        if partno:
            try:
                part = Part.objects.get(partno=partno)
                form = PartForm(request.POST, instance=part)
                if form.is_valid():
                    form.save()
                    context.update({
                        "message": "Saved!",
                    })
                else:
                    context.update({
                        "errors": form.errors.items(),
                    })
                context.update({
                    "mod_part": part,
                })
            except Part.DoesNotExist:
                pass
        q = request.POST.get("q")
        if (q):
            context.update({
                "q": q,
                "parts": Part.search(q),
            })
        else:
            context.update({
                "parts": Part.objects.all(),
            })
        return render(request, template, context)

@login_required
def delete(request):
    if request.method == "POST":
        template = "index.html"
        context = {}
        partno = request.POST.get("partno")
        if partno:
            try:
                part = Part.objects.get(partno=partno)
                part.delete()
                context.update({
                    "message": "Deleted!",
                    "mod_part": part,
                })
            except Part.DoesNotExist:
                pass
        q = request.POST.get("q")
        if (q):
            context.update({
                "q": q,
                "parts": Part.search(q),
            })
        else:
            context.update({
                "parts": Part.objects.all(),
            })
        return render(request, template, context)

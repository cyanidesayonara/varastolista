from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext as _
from django.utils import translation
import tablib
from .resources import PartResource
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

def language(request):
    languages = ["en", "fi"]
    if request.method == "POST":
        language = request.POST.get("language")
        if language and language in languages:
            translation.activate(language)
            request.session[translation.LANGUAGE_SESSION_KEY] = language
    return redirect("/")
    
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
    else:
        raise Http404

@login_required
def new(request):
    if request.method == "POST":
        template = "index.html"
        context = {}
        form = PartForm(request.POST)
        if form.is_valid():
            part, created = Part.objects.get_or_create(**form.cleaned_data)
            message = _("Part added")
            context.update({
                "mod_part": part,
                "message": message,
            })
        else:
            context.update({
                "errors": form.errors.items(),
            })
        context.update({
            "parts": Part.objects.all(),
        })
        return render(request, template, context)
    else:
        raise Http404

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
                message = _("Added (+1)")
                context.update({
                    "message": message,
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
    else:
        raise Http404

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
                message = _("Subtracted (-1)")
                context.update({
                    "message": message,
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
    else:
        raise Http404

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
                    message = _("Saved")
                    context.update({
                        "message": message,
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
    else:
        raise Http404

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
                message = _("Delete")
                context.update({
                    "message": message,
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
    else:
        raise Http404

@login_required
def upload(request):
    if request.method == "POST":
        part_resource = PartResource()
        dataset = tablib.Dataset()
        if request.FILES:
            parts = request.FILES["parts"]

            try:
                imported_data = dataset.load(parts.read())
                result = part_resource.import_data(
                    dataset, dry_run=True)  # Test the data import

                if not result.has_errors():
                    part_resource.import_data(
                        dataset, dry_run=False)  # Actually import now
                    message = _("Parts imported")
                else:
                    message = _("Couldn't import file")
            except tablib.core.UnsupportedFormat:
                message = _("Unsupported format")
        else:
            message = _("No file found")

        template = "index.html"
        context = {}
        user = request.user
        if user.is_authenticated:
            context.update({
                "message": message,
                "parts": Part.objects.all(),
            })
        return render(request, template, context)
    else:
        return redirect("/")

@login_required
def download(request):
    if request.method == "GET":
        part_resource = PartResource()
        dataset = part_resource.export()
        response = HttpResponse(
            dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="parts.xls"'
        return response
    else:
        raise Http404

from django.shortcuts import get_object_or_404, redirect, render

from .models import Color


def index(request):
    return render(request, "color_picker/index.html", {})

def viewer(request):
    colors = Color.objects.all()
    context = {"colors": colors}

    return render(request, "color_picker/viewer.html", context)
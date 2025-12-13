from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from .forms import ColorInterpolationForm
from .models import ColorFamily, Color
from .utils import interpolate


class FamiliesListView(ListView):
    model = ColorFamily


def index(request):
    return render(request, "color_picker/index.html", {})

def viewer(request):
    colors = Color.objects.order_by('family')

    context = {"families": []}
    for c in colors:
        c_fam = c.family

        family_found = False
        for i, fam in enumerate(context['families']):
            if fam['family'] == c_fam:
                family_found = True
                context['families'][i]["colors"].append(c)
        
        if not family_found:
            context['families'].append({"family": c_fam, "colors": [c]})
        
    return render(request, "color_picker/viewer.html", context)

def to_css_parameters(request, family_id):
    family = get_object_or_404(ColorFamily, id=family_id)
    return HttpResponse(family.to_css_parameters().replace('\n', '<br>'))

def generate_colors(request, family_id):
    family = get_object_or_404(ColorFamily, id=family_id)

    if request.method == "POST":
        form = ColorInterpolationForm(request.POST)
        if form.is_valid():
            l_min = form.cleaned_data["l_min"]
            l_max = form.cleaned_data["l_max"]

            c_min = form.cleaned_data["c_min"]
            c_max = form.cleaned_data["c_max"]

            h_min = form.cleaned_data["h_min"]
            h_max = form.cleaned_data["h_max"]

            count = form.cleaned_data["count"]

            for i in range(count):
                t = i / (count - 1) if count > 1 else 0

                L = interpolate(l_min, l_max, t)
                C = interpolate(c_min, c_max, t)
                h = interpolate(h_min, h_max, t)

                Color.objects.create(
                    family=family,
                    mode="oklch",
                    values={"l": L, "c": C, "h": h},
                )

            return redirect("families_list")

    else:
        form = ColorInterpolationForm()

    return render(request, "color_picker/generate_colors.html", {
        "family": family,
        "form": form,
    })

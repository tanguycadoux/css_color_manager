from django.urls import path

from .views import index, viewer, generate_colors, FamiliesListView


urlpatterns = [
    path('', index, name="index"),
    path('viewer/', viewer, name="viewer"),
    path('families/', FamiliesListView.as_view(), name="families_list"),
    path('generate_colors/<int:family_id>', generate_colors, name="generate_colors"),
]
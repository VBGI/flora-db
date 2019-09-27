from django.shortcuts import render
from django.views.generic.detail import DetailView, ListView
from .models import Family, Genus, Species


class FamilyDetailView(DetailView):
    model = Family

class GenusDetailView(DetailView):
    model = Genus

class SpeciesDetailView(DetailView):
    model = Species

class LinkDetailView(DetailView):
    model = Link

class FamilyListView(ListView):
    model = List

class GenusListView(ListView):
    model = Genus


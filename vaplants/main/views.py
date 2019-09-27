from django.shortcuts import render
from django.views.generic.detail import DetailView, ListView
from .models import Family, Genus, Species, Page, Link


class FamilyDetailView(DetailView):
    template_name = "common_entity.html"
    model = Family


class GenusDetailView(DetailView):
    template_name = "common_entity.html"
    model = Genus


class SpeciesDetailView(DetailView):
    template_name = "common_entity.html"
    model = Species


class LinkDetailView(DetailView):
    template_name = "common_entity.html"
    model = Link


class PageDetailView(DetailView):
    template_name = "page.html"
    model = Page


class FamilyListView(ListView):
    model = Family


class GenusListView(ListView):
    model = Genus



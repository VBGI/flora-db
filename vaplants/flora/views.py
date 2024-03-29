from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, View
from django.db.models import Q
from .models import Family, Genus, Species, Page, Link, TitleImage, Occurrence, Location



class TitleMixinView:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_images'] = TitleImage.objects.all()
        context['pages'] = Page.objects.filter(public=True)
        return context


class CommonDetailView(TitleMixinView, DetailView):
    template_name = "common_entity.html"


class FamilyDetailView(CommonDetailView):
    model = Family
    slug_field = 'name'
    slug_url_kwarg = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        coordinates = []
        species_model = ContentType.objects.get(model="family")
        occurrences = Occurrence.objects.filter(content_type=species_model,
                                                object_id=obj.id)
        for occur in occurrences:
            if occur.area:
                coordinates.append(occur.area)
            elif occur.location_id:
                coordinates.append(occur.location.area)
        context['coordinates'] = coordinates
        return context


class GenusDetailView(CommonDetailView):
    model = Genus
    slug_field = 'name'
    slug_url_kwarg = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        coordinates = []
        species_model = ContentType.objects.get(model="genus")
        occurrences = Occurrence.objects.filter(content_type=species_model,
                                                object_id=obj.id)
        for occur in occurrences:
            if occur.area:
                coordinates.append(occur.area)
            elif occur.location_id:
                coordinates.append(occur.location.area)
        context['coordinates'] = coordinates
        return context


class LocationDetailView(CommonDetailView):
    template_name = "location_entity.html"
    model = Location
    slug_field = 'name'
    slug_url_kwarg = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        coordinates = []
        coordinates.append(obj.area)
        context['coordinates'] = coordinates
        return context


class OccurrenceDetailView(CommonDetailView):
    template_name = "occurrence_entity.html"
    model = Occurrence

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        coordinates = []
        if obj.area:
            coordinates.append(obj.area)
        elif obj.location_id:
            coordinates.append(obj.location.area)
        context['coordinates'] = coordinates
        return context


class SpeciesDetailView(CommonDetailView):
    model = Species

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        coordinates = []
        species_model = ContentType.objects.get(model="species")
        occurrences = Occurrence.objects.filter(content_type=species_model,
                                                object_id=obj.id)
        for occur in occurrences:
            if occur.area:
                coordinates.append(occur.area)
            elif occur.location_id:
                coordinates.append(occur.location.area)
        context['coordinates'] = coordinates
        return context


class PageView(TitleMixinView, DetailView):
    template_name = "page.html"
    model = Page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['species'] = Species.objects.all()
        return context


class CommonListView(TitleMixinView, ListView):
    template_name = "common_list.html"
    paginate_by = 100


class LocationListView(CommonListView):
    model = Location

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_name'] = 'Locations'
        context['model_url_name'] = 'location-detail'
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(name__icontains=self.kwargs.get('q', ''),
                               name__istartswith=self.kwargs.get('fl', ''))


class SpeciesListView(CommonListView):
    model = Species

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_name'] = 'Species'
        context['model_url_name'] = 'species-detail'
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(name__icontains=self.kwargs.get('q', ''),
                               genus__name__istartswith=self.kwargs.get('fl', ''))


class FamilyListView(CommonListView):
    model = Family

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_name'] = 'Families'
        context['model_url_name'] = 'family-detail'
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(name__icontains=self.kwargs.get('q', ''),
                               name__istartswith=self.kwargs.get('fl', ''))

class GenusListView(CommonListView):
    model = Genus

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_name'] = 'Genera'
        context['model_name'] = 'Genera'
        context['model_url_name'] = 'genus-detail'
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(name__icontains=self.kwargs.get('q', ''),
                               name__istartswith=self.kwargs.get('fl', ''))



class SearchView(TitleMixinView, TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        context['families'] = Family.objects.filter(Q(info__icontains=q)|
                                                    Q(name__icontains=q))
        context['genera'] = Genus.objects.filter(Q(info__icontains=q)|
                                                 Q(name__icontains=q))
        context['species'] = Species.objects.filter(Q(info__icontains=q)|
                                                    Q(genus__name__icontains=q)|
                                                    Q(name__icontains=q))
        context['locations'] = Location.objects.filter(Q(info__icontains=q)|
                                                    Q(name__icontains=q))
        # context['species'] = Species.objects.filter(Q(info__icontains=q)|
        #                                             Q(genus__name__icontains=q)|
        #                                             Q(name__icontains=q)|
        #                                             Q(occurrences__name__icontains=q)|
        #                                             Q(occurrences__info__icontains=q)
        #                                             )
        return context


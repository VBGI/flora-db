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


class GenusDetailView(CommonDetailView):
    model = Genus
    slug_field = 'name'
    slug_url_kwarg = 'name'


class LocationDetailView(CommonDetailView):
    model = Location
    slug_field = 'name'
    slug_url_kwarg = 'name'


class OccurrenceDetailView(CommonDetailView):
    model = Occurrence


class SpeciesDetailView(CommonDetailView):
    model = Species


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


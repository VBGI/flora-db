from django.urls import path
from flora.views import (FamilyDetailView, GenusDetailView, SpeciesDetailView,
                        FamilyListView, GenusListView, SpeciesListView, 
                        SearchView, LinkDetailView, PageView)

urlpatterns = [
    path('family/<int:pk>/', FamilyDetailView.as_view(), name='family-detail'),
    path('genus/<int:pk>/', GenusDetailView.as_view(), name='genus-detail'),
    path('species/<int:pk>/', SpeciesDetailView.as_view(), name='species-detail'),
    path('link/<int:pk>/', LinkDetailView.as_view(), name='link-detail'),
    path('search/', SearchView.as_view(), name='search-view'),
    path('families/', FamilyListView.as_view(), name='family-list'),
    path('genera/', GenusListView.as_view(), name='genus-list'),
    path('species/', SpeciesListView.as_view(), name='species-list'),
    path('/', SpeciesListView.as_view(), name='main-page'),
    path('<slug:slug>', PageView.as_view(), name='page-view'),
]
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from .models import Family, Genus, Species
from .serializers import (UserSerializer, FamilySerializer, GenusSerializer, 
                          SpeciesSerializer)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

# REST generic views

class FamilyViewSet(generics.ListAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer


class GenusViewSet(generics.ListAPIView):
    queryset = Genus.objects.all()
    serializer_class = GenusSerializer


class SpeciesViewSet(generics.ListAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
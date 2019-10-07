from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import get_user_model
from .models import Family, Genus, Species
from .serializers import (UserSerializer, FamilySerializer, GenusSerializer, 
                          SpeciesSerializer)


# REST generic views


class UserList(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class FamilyViewSet(generics.ListCreateAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer


class GenusViewSet(generics.ListCreateAPIView):
    queryset = Genus.objects.all()
    serializer_class = GenusSerializer


class SpeciesViewSet(generics.ListCreateAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
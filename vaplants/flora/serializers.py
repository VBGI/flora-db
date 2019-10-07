from django.contrib.auth.models import User 
from rest_framework import serializers
from .models import Genus, Family, Species


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']

class GenusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genus
        fields = ['url', 'username', 'email', 'groups']


class SpeciesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Species
        fields = ['url', 'name']

class FamilySerializer(serializers.):
    class Meta:
        model = Family
        fields = []


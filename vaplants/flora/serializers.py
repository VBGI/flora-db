from django.contrib.auth.models import User 
from rest_framework import serializers
from .models import Genus, Family, Species

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']


class GenusSerializer(serializers.HyperlinkedModelSerializer):
    family_name = serializers.CharField(source='family.name')

    class Meta:
        model = Genus
        fields = ['name', 'info', 'family_name']


class SpeciesSerializer(serializers.HyperlinkedModelSerializer):
    genus_name = serializers.CharField(source='genus.name')
    family_name = serializers.CharField(source='genus.family.name')

    class Meta:
        model = Species
        fields = ['name']

class FamilySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Family
        fields = ['name', 'info']


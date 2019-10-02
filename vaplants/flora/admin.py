from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import *


class SpeciesSynonimInline(admin.TabularInline):
    model = SpeciesSynonim
    fk_name = 'from_species'
    extra = 1

class LinkAdminInline(GenericTabularInline):
    model = Link
    extra = 1

class OccurrenceAdminInline(GenericTabularInline):
    model = Occurrence
    fields = ('name', 'info')
    extra = 1

class SpeciesAdmin(admin.ModelAdmin):
    inlines = (SpeciesSynonimInline, LinkAdminInline, OccurrenceAdminInline)
    fields = ('genus', 'name', 'rarity', 'info')

class FamilyAdmin(admin.ModelAdmin):
    inlines = (LinkAdminInline, OccurrenceAdminInline)
    fields = ('name', 'rarity', 'info')

class GenusAdmin(admin.ModelAdmin):
    fields = ('family', 'name', 'rarity', 'info')
    inlines = (LinkAdminInline, OccurrenceAdminInline)

    



admin.site.register(Species, SpeciesAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(Genus, GenusAdmin)
admin.site.register([Page, TitleImage])


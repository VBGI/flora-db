from django.contrib import admin
from .models import *


class SpeciesSynonimInline(admin.TabularInline):
    model = SpeciesSynonim
    fk_name = 'from_species'
    extra = 1

class SpeciesAdmin(admin.ModelAdmin):
    inlines = (SpeciesSynonimInline, )
    

admin.site.register(Species, SpeciesAdmin)
admin.site.register([Page, Family, Genus, Link, TitleImage,
                     Occurrence])


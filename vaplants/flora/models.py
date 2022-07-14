from django.db import models
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.safestring import mark_safe
from django.urls import reverse


class UpdaterMixin(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), null=True, blank=True,
                             on_delete=models.SET_NULL, editable=False)

    class Meta:
        abstract = True


class RarityMixin(models.Model):
    RARITY_CHOICES = (
                      ('R', 'Regular'),
                      ('E', 'Endanger'),
                      ('V', 'Vanishing'),
                      )
    rarity = models.CharField(choices=RARITY_CHOICES, max_length=1, default='R',
                              blank=True, null=True)

    class Meta:
        abstract = True


class InfoMixin(models.Model):
    name = models.CharField(max_length=50, default='')
    info = models.TextField(blank=True, default='', null=False)

    class Meta:
        ordering = ('name', )
        abstract = True

    def __str__(self):
        return self.name.title()

    def clean(self):
        self.name = self.name.strip().lower()
    
    @property
    def full_name_as_html(self):
        return self.__str__()



class ForeignRelationMixin(models.Model):
    allowed_models = models.Q(app_label='flora', model='family') | \
                     models.Q(app_label='flora', model='genus') | \
                     models.Q(app_label='flora', model='species')
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to=allowed_models,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class Family(UpdaterMixin, InfoMixin, RarityMixin):
    links = GenericRelation('Link', related_query_name='family')
    occurrences = GenericRelation('Occurrence', related_query_name='family')

    class Meta(InfoMixin.Meta):
        verbose_name_plural = 'Families'
        verbose_name = 'Family'

    def get_absolute_url(self):
        return reverse('family-detail', args=[self.name])


class Genus(UpdaterMixin, InfoMixin, RarityMixin):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    links = GenericRelation('Link', related_query_name='genus')
    occurrences = GenericRelation('Occurrence', related_query_name='genus')

    class Meta(InfoMixin.Meta):
        verbose_name_plural = 'Genera'
        verbose_name = 'Genus'

    def get_absolute_url(self):
        return reverse('genus-detail', args=[self.name])


class Location(UpdaterMixin, InfoMixin):
    name = models.CharField(max_length=300, default='')
    abbr = models.CharField(max_length=10, default='')
    area = models.CharField(max_length=300, default='')

    class Meta(InfoMixin.Meta):
        verbose_name_plural = 'Locations'
        verbose_name = 'Location'

    def get_absolute_url(self):
        return reverse('location-detail', args=[self.name])


class Species(UpdaterMixin, InfoMixin, RarityMixin):
    authorship = models.CharField(max_length=50, default='', blank=True)
    genus = models.ForeignKey(Genus, blank=False, on_delete=models.CASCADE)
    synonym = models.ManyToManyField('self', through='SpeciesSynonim',
                                     symmetrical=False,
                                     through_fields=('from_species',
                                                     'to_species'),
                                     related_name='+'
                                     )
    links = GenericRelation('Link', related_query_name='species')
    occurrences = GenericRelation('Occurrence', related_query_name='species')

    class Meta:
        ordering = ('genus__name', 'name')
        verbose_name_plural = 'Species'
        verbose_name = 'Species'

    def __str__(self):
        return self.full_name

    def clean(self):
        pass

    def get_absolute_url(self):
        return reverse('species-detail', args=[str(self.id)])

    @property
    def full_name(self):
        return '{} {}'.format(self.genus, self.name)

    @property
    def full_name_as_html(self):
        return mark_safe('<em>{} {}</em> {}'.format(self.genus, self.name, self.authorship))

class SpeciesSynonim(models.Model):
    SYN_CHOICES = (
                   ('K', 'Kharkevich'),
                   ('Q', 'QIAN')
                   )
    from_species = models.ForeignKey(Species, related_name='related_from',
                                     on_delete=models.CASCADE)
    to_species = models.ForeignKey(Species, related_name='related_to',
                                    on_delete=models.CASCADE)
    synonym_table = models.CharField(max_length=1,
                                     choices=SYN_CHOICES, default='N')


class Link(UpdaterMixin, ForeignRelationMixin):
    title = models.CharField(max_length=500, default='')
    url = models.URLField(max_length=500, default='')


class Occurrence(UpdaterMixin, ForeignRelationMixin, InfoMixin):
    name = models.CharField(max_length=300, default='')
    abbr = models.CharField(max_length=10, default='', blank=True)
    location = models.ForeignKey(Location, default=None, blank=True,
                                 related_name='occurrences', on_delete=models.CASCADE)
    area = models.CharField(max_length=300, default='', blank=True)

    def __str__(self):
        return self.name.title()

    def get_absolute_url(self):
        return reverse('occurrence-detail', args=[str(self.pk)])

    # TODO: Postgres + PostGIS
    # points = models.MultiPointfield()
    # polygons = models.MultiPolygonField()


class Page(models.Model):
    title = models.CharField(max_length=15, default='')
    text = models.TextField(default='', blank=True)
    slug = models.SlugField(default='')
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:80]

    def get_absolute_url(self):
        return reverse('page-detail', args=[str(self.slug)])


class TitleImage(models.Model):
    image = models.ImageField(upload_to='title_images/', blank=True,
                              max_length=500)
    caption = models.TextField(default='', blank=True)

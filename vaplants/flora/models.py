from django.db import models
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property
from django.urls import reverse


class UpdaterMixin(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeingKey(get_user_model(), null=True, blank=True,
                             on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class RarityMixin(models.Model):
    RARITY_CHOICES = (
                      ('R', 'Regular'),
                      ('E', 'Endanger'),
                      ('V', 'Vanishing'),
                      )
    rarity = models.CharField(choices=RARITY_CHOICES, default='',
                              blank=True, null=True)

    class Meta:
        abstract = True


class InfoMixin(models.Model):
    info = models.TextField(blank=True, default='', null=False)

    class Meta:
        abstract = True


class Family(UpdaterMixin, InfoMixin, RarityMixin):
    family = models.CharField(max_length=50, default='')

    class Meta:
        ordering = ('family', )
        verbose_name_plural = 'Families'
        verbose_name = 'Family'

    def __str__(self):
        return self.family

    def get_absolute_url(self):
        return reverse('family-detail', args=[str(self.id)])

    def clean(self):
        self.family = self.family.strip().lower()


class Genus(UpdaterMixin, InfoMixin, RarityMixin):
    genus = models.CharField(max_length=50, default='')
    family = models.ForeingKey(Family)

    class Meta:
        ordering = ('genus', )
        verbose_name_plural = 'Genuses'
        verbose_name = 'Genus'

    def __str__(self):
        return self.genus

    def get_absolute_url(self):
        return reverse('genus-detail', args=[str(self.id)])

    def clean(self):
        self.genus = self.genus.strip().lower()


class Species(UpdaterMixin, InfoMixin, RarityMixin):
    epithet = models.CharField(max_length=50, default='', blank=True,
                               verbose_name='species epithet')
    authorship = models.CharField(max_length=50, default='', blank=True)
    genus = models.ForeingKey(Genus, blank=False)

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('species-detail', args=[str(self.id)])

    @property
    def full_name(self):
        return f'{self.genus} {self.epithet}'


class Link(models.Model):
    title = models.CharField(max_length=500, default='')
    url = models.UrlField(max_length=500, default='')
    species = models.ForeingKey(Species, null=True, blank=True)
    genus = models.ForeingKey(Genus, null=True, blank=True)
    family = models.ForeingKey(Family, null=True, blank=True)

    def __str__(self):
        if self.family:
            return f'{self.url} : Family: {self.family.family}'
        elif self.genus:
            return f'{self.url} : Genus: {self.genus.genus}'
        elif self.species:
            return f'{self.url} : Species: {self.species}'
        return f"Unreferenced link object: {self.pk}"

    def get_absolute_url(self):
        return reverse('link-detail', args=[str(self.id)])


class Occurrence(InfoMixin):
    name = models.CharField(max_length=300, defualt='')
    description = models.TextField(blank=True, default='')

    # TODO: will be added when migratin to Postgres + PostGIS
    # points = models.MultiPointfield()
    # polygons = models.MultiPolygonField()

    species = models.ForeingKey(Species, blank=True, null=True)
    genus = models.ForeingKey(Genus, blank=True, null=True)
    family = models.ForeingKey(Family, blank=True, null=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    title = models.CharField(max_length=15, default='')
    text = models.TextField(default='', blank=True)
    slug = models.SlugField(default='')
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:80]

    def get_absolute_url(self):
        return reverse('page-detail', args=[str(self.id)])


class TitleImage(models.Model):
    image = models.ImageField(upload_to='title_images/', blank=True,
                              max_legnth=500)
    caption = models.TextField(default='', blank=True)

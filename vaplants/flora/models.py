from django.db import models
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property
from django.urls import reverse


class UpdaterMixin(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), null=True, blank=True,
                             on_delete=models.SET_NULL)

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
    family = models.ForeignKey(Family, on_delete=models.CASCADE)

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
    genus = models.ForeignKey(Genus, blank=False, on_delete=models.CASCADE)
    synonym = models.ManyToManyField('self', through='SpeciesSynonim',
                                     symmetrical=False,
                                     through_fields=('from_species',
                                                     'to_species'),
                                     related_name='+'
                                     )

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('species-detail', args=[str(self.id)])

    @property
    def full_name(self):
        return f'{self.genus} {self.epithet}'


class SpeciesSynonim(models.Model):
    SYN_CHOICES = (
                   ('N', 'Normal'),
                   ('A', 'Advanced')
                   )
    from_species = models.ForeignKey(Species, related_name='related_from',
                                     on_delete=models.CASCADE)
    to_species = models.ForeignKey(Species, related_name='related_to',
                                    on_delete=models.CASCADE)
    synonym_table = models.CharField(max_length=1,
                                     choices=SYN_CHOICES, default='N')


class Link(models.Model):
    title = models.CharField(max_length=500, default='')
    url = models.URLField(max_length=500, default='')
    species = models.ForeignKey(Species, null=True, blank=True,
                                on_delete=models.CASCADE)
    genus = models.ForeignKey(Genus, null=True, blank=True,
                              on_delete=models.CASCADE)
    family = models.ForeignKey(Family, null=True, blank=True,
                               on_delete=models.CASCADE)

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
    name = models.CharField(max_length=300, default='')
    description = models.TextField(blank=True, default='')

    # TODO: will be added when migratin to Postgres + PostGIS
    # points = models.MultiPointfield()
    # polygons = models.MultiPolygonField()

    species = models.ForeignKey(Species, blank=True, null=True,
                                on_delete=models.CASCADE)
    genus = models.ForeignKey(Genus, blank=True, null=True,
                              on_delete=models.CASCADE)
    family = models.ForeignKey(Family, blank=True, null=True,
                               on_delete=models.CASCADE)

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
                              max_length=500)
    caption = models.TextField(default='', blank=True)

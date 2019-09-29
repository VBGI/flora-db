from django.test import TestCase, Client

from .models import Genus, Species, Family, Page, Link, TitleImage

# Create your tests here.

def generate_fake_data(cls):
    family = Family.objects.create(family="Awesome", info="awesome_family")
    genus = Genus.objects.create(family=family, info="awesome_genus",
                                 genus="noname_genus", id=1)
    species = Species.objects.create(genus=genus, info="awesome_species")
    Link.objects.create(family=family, url="http://example.com/family")
    Link.objects.create(genus=genus, url="http://example.com/genus")
    Link.objects.create(species=species, url="http://example.com/species")
    cls.family = family
    cls.genus = genus
    cls.species = species
    cls.page = Page.objects.create(title='awesome page',
                                   text='unique page content')
    cls.titleImage = TitleImage.objects.create(caption='unique title image')


class GeneraTest(TestCase):

    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        generate_fake_data(cls)
        

    def test_main(self):
        response =self.client.get('/genus/1')
        
    def test2(self):
        # Some other test using self.foo
        ...
from django.test import TestCase, Client

from .models import Genus, Species, Family, Page, Link, TitleImage


def generate_fake_data(cls):
    family = Family.objects.create(name="Awesome", info="AwesomeFamily", id=1)
    genus = Genus.objects.create(family=family, info="awesome_genus",
                                 name="nonamegenus", id=1)
    species = Species.objects.create(genus=genus, info="awesome_species", name="SP1")

    Link.objects.create(content_object=family, url="http://example.com/family", id=1)
    Link.objects.create(content_object=genus, url="http://example.com/genus", id=2)
    Link.objects.create(content_object=species, url="http://example.com/species", id=3)

    cls.family = family
    cls.genus = genus
    cls.species = species
    cls.page = Page.objects.create(title='awesome page',
                                   text='unique page content')
    cls.titleImage = TitleImage.objects.create(caption='unique title image')


class GeneralEntityTest(TestCase):

    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        generate_fake_data(cls)


class GeneraTest(GeneralEntityTest):
    
    def setUp(self):
        super().setUp()
        self.response = self.client.get('/genus/1', follow=True)

    def test_genus_page_200(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_genus_page_content(self):
        self.assertIn(b'awesome_genus', self.response.content)
        self.assertIn(b'Nonamegenus', self.response.content)
        
    def test_related_link_inclusion(self):
        self.assertIn(b'http://example.com/genus', self.response.content)


class FamilyTest(GeneralEntityTest):

    def setUp(self):
        super().setUp()
        self.response = self.client.get('/family/1', follow=True)

    def test_family_page_200(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_family_page_content(self):
        self.assertIn(b'Awesome', self.response.content)
        self.assertIn(b'AwesomeFamily', self.response.content)
        
    def test_related_link_inclusion(self):
        self.assertIn(b'http://example.com/family', self.response.content)
    

class SpeciesTest(GeneralEntityTest):

    def setUp(self):
        super().setUp()
        self.response = self.client.get('/species/1', follow=True)    
    
    def test_species_page_200(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_species_page_content(self):
        self.assertIn(b'SP1', self.response.content)
    
    def test_related_link_inclusion(self):
        self.assertIn(b'http://example.com/species', self.response.content)

    def test_genus_name_exists(self):
        self.assertIn(b'Nonamegenus', self.response.content)
    
class TestPageView(GeneralEntityTest):
    def setUp(self):
        super().setUp()
        self.response  = self.client.get('/')

    def test_image_included(self):
        self.assertIn(b'unique title image', self.response.content)

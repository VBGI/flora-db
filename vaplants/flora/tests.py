from django.test import TestCase, Client

from .models import Genus, Species, Family, Page, Link, TitleImage

# Create your tests here.

def generate_fake_data(cls):
    family = Family.objects.create(family="Awesome", info="awesome_family", id=1)
    genus = Genus.objects.create(family=family, info="awesome_genus",
                                 genus="noname_genus", id=1)
    species = Species.objects.create(genus=genus, info="awesome_species")
    Link.objects.create(family=family, url="http://example.com/family", id=1)
    Link.objects.create(genus=genus, url="http://example.com/genus", id=2)
    Link.objects.create(species=species, url="http://example.com/species", id=3)
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
        

    def test_genus_page_200(self):
        response =self.client.get('/genus/1')
        self.assertEqual(response.status_code, 200)
    
    def test_genus_page_content(self):
        response =self.client.get('/genus/1')
        self.assertInHTML(b'awesome_genus', response.content)
        self.assertInHTML(b'noname_genus', response.content)
        
    def test_related_link_inclusion(self):
        response = self.client.get('/genus/1')
        self.assertInHTML(b'http://example.com/genus', response.content)



class LinkTest(TestCase):

    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        generate_fake_data(cls)
        

    def test_link_page_200(self):
        response =self.client.get('/link/1')
        self.assertEqual(response.status_code, 200)
  

class FamilyTest(TestCase):

    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        generate_fake_data(cls)
        

    def test_family_page_200(self):
        response =self.client.get('/family/1')
        self.assertEqual(response.status_code, 200)
    
    def test_family_page_content(self):
        response =self.client.get('/family/1')
        self.assertInHTML(b'Awesome', response.content)
        self.assertInHTML(b'awesome_family', response.content)
        
    def test_related_link_inclusion(self):
        response = self.client.get('/family/1')
        self.assertInHTML(b'http://example.com/family', response.content)
    


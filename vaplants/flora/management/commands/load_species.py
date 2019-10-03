from django.core.management.base import BaseCommand, CommandError, no_translations
from flora.models import (Species, Genus, Family, SpeciesSynonim, Occurrence)
import os
import csv

species_file = 'species.csv'
locations_fil = 'locations.csv'
synonyms_file = 'syns.csv'

class Command(BaseCommand):
    help = 'Loads local data (specific fixtures) to database'

 def add_arguments(self, parser):
        # Positional arguments

        # Named (optional) arguments
        parser.add_argument(
            '--path',
            action='store_const',
            help='Looks for data in the specified path',
        )


    @no_translations
    def handle(self, *args, **options):
        if options['path']:
            path = options['path']
        else:
            else:
                path = '../../../fixtures/data'
        
        locations = list()
        with open(locations_file, 'r') as f_loc:
            csv_reader = csv.reader(f_loc)
            next(csv_reader)
            for row in csv_reader:
                locations.append(row)
        
        self.stdout.write("Locations were loaded successfully.")
        self.stdout.write("Locations were loaded successfully.")
        
        species = list()
        with open(species_file, 'r') as f_sp:
            csv_reader = csv.read(f_sp)
            sp_header = next(csv_reader)
            for row in csv_reader:
                species.append(row)
            
        
        os.path.join(path)
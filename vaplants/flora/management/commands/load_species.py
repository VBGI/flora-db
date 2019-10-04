from django.core.management.base import BaseCommand, CommandError, no_translations
from django.contrib.contenttypes.models import ContentType
from flora.models import (Species, Genus, Family, SpeciesSynonim, Occurrence)
import os
import csv

species_file = 'species.csv'
locations_file = 'locations.csv'
synonyms_file = 'syns.csv'

class Command(BaseCommand):
    help = 'Loads local data (specific fixtures) to database'

    def add_arguments(self, parser):
            # Positional arguments

            # Named (optional) arguments
            parser.add_argument('--path', type=str,
                help='Looks for data in the specified path',
            )

    @staticmethod
    def parse_genus(s):
        if len(s.strip().split()) < 2:
            return 'none'
        else:
            return s.strip().split()[0]

    @no_translations
    def handle(self, *args, **options):
        if options['path']:
            path = options['path']
        else:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../fixtures/data')
        self.stdout.write("Current path = %s" % path)

        locations = dict()
        with open(os.path.join(path, locations_file), 'r') as f_loc:
            csv_reader = csv.reader(f_loc)
            next(csv_reader)
            for row in csv_reader:
                locations.setdefault(row[1], row[0])
        self.stdout.write("Locations were loaded successfully.")
        
        species = list()
        with open(os.path.join(path, species_file), 'r') as f_sp:
            csv_reader = csv.reader(f_sp)
            sp_header = next(csv_reader)
            for row in csv_reader:
                species.append(row)
        self.stdout.write("Species were loaded: total number of rows: %s" % len(species))
        self.stdout.write(str(sp_header))

        # Create species instances
        for row in species:
            authorship = row[2].strip()
            family, _ = Family.objects.get_or_create(name=row[0].lower().strip())
            genus, _ = Genus.objects.get_or_create(name=self.parse_genus(row[1]), family=family)
            species, _ = Species.objects.get_or_create(genus=genus, name=row[1].strip().lower())
            sp_content_type = ContentType.objects.get(model='species')
            
            for val, loc in zip(row[3:], sp_header[3:]):
                if val and val.strip():
                    occurrence, _ = Occurrence.objects.get_or_create(content_type=sp_content_type, object_id=species.pk, name=locations.get(loc,'Not defined'))
            
            self.stdout.write("Processing species: %s" % row[1])
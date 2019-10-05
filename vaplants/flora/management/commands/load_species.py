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
                locations.setdefault(row[2], row[0])
        self.stdout.write("Locations were loaded successfully.")
        
        species = list()
        with open(os.path.join(path, species_file), 'r') as f_sp:
            csv_reader = csv.reader(f_sp)
            sp_header = next(csv_reader)
            for row in csv_reader:
                species.append(row)
        self.stdout.write("Species were loaded: total number of rows: %s" % len(species))
        self.stdout.write(str(sp_header))


        syns = list()
        with open(os.path.join(path, synonyms_file), 'r') as f_syn:
            csv_reader = csv.reader(f_syn)
            next(csv_reader)
            for row in csv_reader:
                syns.append(row)
        self.stdout.write("Synonyms were loaded: total number of rows: %s" % len(syns))

        # Create species instances
        for row in species:
            authorship = row[2].strip()
            family, _ = Family.objects.get_or_create(name=row[0].lower().strip())
            genus, _ = Genus.objects.get_or_create(name=self.parse_genus(row[1]),
                                                   family=family)
            species, _ = Species.objects.get_or_create(genus=genus,
                                                       name=row[1].strip().lower().replace(self.parse_genus(row[1]).lower(), ''),
                                                       authorship=authorship,
                                                       )
            sp_content_type = ContentType.objects.get(model='species')
            
            for val, loc in zip(row[3:], sp_header[3:]):
                if val and val.strip():
                    occurrence, _ = Occurrence.objects.get_or_create(content_type=sp_content_type,
                                                                     object_id=species.pk,
                                                                     name=locations.get(loc,'Not defined'), abbr=loc)
            
            
            self.stdout.write("Processing species: %s" % row[1])
        
        self.stdout.write("Preliminary list of species is loaded")

        for row in syns: 
            sp_name = row[6].strip().lower().replace(self.parse_genus(row[6]).lower(), '')
            genus_name = self.parse_genus(row[6])
            authorship = row[7].strip()
            family_name = row[1].strip().lower()
            
            if not sp_name.strip():
                continue

            # find family
            qs = Species.objects.filter(name__iexact=sp_name, genus__name__iexact=genus_name)
            sp = None
            if not qs.exists():
                # species creation
                family, _ = Family.objects.get_or_create(name__iexact=family_name)
                genus, _ = Genus.objects.get_or_create(name__iexact=genus_name, family=family)
                sp, _ = Species.objects.get_or_create(name=sp_name, genus=genus)
            
            if sp:
                sp = qs.first()
            sp.authorship = authorship
            sp.save()
            self.stdout.write("Clarifying authorship: %s" % sp.full_name)
        self.stdout.write("All data is loaded.")

            # FIXME: Impossible to understand synonyms fixture.
            # code_khark = row[3]
            # for srow in syns:
            #     s_c = srow[0]
            #     s_name = srow[6].strip().lower().replace(self.parse_genus(row[1]).lower()
            #     s_auth = srow[7].strip()

            #     sfamily, _ = Family.objects.get_or_create(name__iexact=srow[1].strip().lower())
            #     sgenus, _ = Genus.objects.get_or_create(name__iexact=self.parse_genus(srow[6]), family=sfamily)
            #     ssp, _ = Species.objects.get_or_create(name__iexact=)
            #     ssp = 

            # for c, name, author in zip(syns[0], )
            # SpeciesSynonim(from_sp, to_sp)


            


        


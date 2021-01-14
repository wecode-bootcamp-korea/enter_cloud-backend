from faker import Faker
from django_seed import Seed

from django.core.management.base import BaseCommand

from spaces.models  import *
from my_settings    import tag_list, type_list, week_list, facilities_informations, detail_facility_list

class Command(BaseCommand):
    help = "create tags"

    def handle(self, *args, **options):
        
        for tag in tag_list:
            Tag.objects.create(name = tag)
        
        for space_type in type_list:
            Type.objects.create(name = space_type)

        for day in week_list:
            BreakDay.objects.create(day = day)

        for description in facilities_informations:
            Facility.objects.create(description = description)

        for detail_facility in detail_facility_list:
            DetailFacility.objects.create(name = detail_facility)

        for detail_type in type_list:
            DetailType.objects.create(name = detail_type)
        self.stdout.write(self.style.SUCCESS(f'Option list created'))
        
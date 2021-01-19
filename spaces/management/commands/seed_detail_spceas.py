import csv
import random
import bcrypt
from django_seed import Seed
from faker       import Faker

from django.contrib.admin.utils     import flatten
from django.core.management.base    import BaseCommand
from django.utils                   import timezone
from django.db.models               import Count

from users.models   import Host
from spaces.models  import (Space,
                            Tag,
                            Facility,
                            BreakDay,
                            Type,
                            SubImage,
                            SpaceFacility,
                            SpaceTag,
                            SpaceBreakday,
                            DetailSpace,
                            DetailType,
                            DetailFacility)
from my_settings    import (name_list,
                            simple_info_list, 
                            main_info_list, 
                            detail_name_list, 
                            detail_facility_list)

class Command(BaseCommand):

    help = "create detail spaces"

    def handle(self, *args, **options):
        number              = 2
        spaces              = Space.objects.all()
        file                = open("all.csv", mode="r")
        reader              = file.readlines()
        image_length        = len(reader)
        detail_types        = DetailType.objects.all()
        detail_facilities   = DetailFacility.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            DetailSpace,
            number,
            {
                "space":                  lambda x : random.choice(spaces) if spaces.aggregate(Count("detailspace"))["detailspace__count"] < 3 else random.choice(spaces),
                "name":                   lambda x : random.choice(detail_name_list),
                "information":            lambda x : random.choice(main_info_list),
                "image":                  lambda x : reader[random.randint(0, image_length-1)],
                "min_reservation_time":   lambda x : random.randint(2, 5),
                "min_people":             lambda x : random.randint(1, 2),
                "max_people":             lambda x : random.randint(4, 10),
                "price":                  10000,
            }
        )
        seed_detail_space       = seeder.execute()
        detail_space_id_list    = flatten(seed_detail_space.values())
        
        for detail_space_id in detail_space_id_list:
            detail_space        = DetailSpace.objects.get(id = detail_space_id)
        
            random_number       = random.randint(1, len(detail_types))
            detail_type_list    = detail_types[random_number:random_number + 2]
            detail_space.detailtype_set.set(detail_type_list)

            random_number           = random.randint(1, len(detail_facilities))
            detail_facility_list    = detail_facilities[random_number:random_number + 6]
            detail_space.detailfacility_set.set(detail_facility_list)
        
        self.stdout.write(self.style.SUCCESS(f'spaces created {number}'))
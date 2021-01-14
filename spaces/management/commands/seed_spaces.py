import csv
import random
import bcrypt
from django_seed import Seed
from faker       import Faker

from django.contrib.admin.utils     import flatten
from django.core.management.base    import BaseCommand
from django.utils                   import timezone

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
    help = "create spaces"

    def add_arguments(self, parser):
        parser.add_argument("--number", type=int, default=1)

    def handle(self, *args, **options):
        number              = options.get("number")
        file                = open("all.csv", mode="r")
        reader              = file.readlines()
        image_length        = len(reader)
        seeder              = Seed.seeder()
        hosts               = Host.objects.all()
        tags                = Tag.objects.all()
        facilities          = Facility.objects.all()
        breakdays           = BreakDay.objects.all()
        types               = Type.objects.all()
        detail_types        = DetailType.objects.all()
        detail_facilities   = DetailFacility.objects.all()
        fake                = Faker(["ko_KR"])
        seeder.add_entity(
            Space,
            number,
            {
                "host":                 lambda x : random.choice(hosts),
                "name":                 lambda x : random.choice(name_list),
                "main_image":           lambda x : reader[random.randint(0, image_length-1)],
                "main_information":     lambda x : random.choice(main_info_list),
                "simple_information":   lambda x : random.choice(simple_info_list),
                "phone_number":         lambda x : fake.phone_number(),
                "main_phone_number":    lambda x : fake.phone_number(),
                "open_time":            lambda x : random.randint(0, 8),
                "close_time":           lambda x : random.randint(20, 24),
                "location":             lambda x : fake.borough(),
                "created_at":           lambda x : timezone.localtime(),
                "updated_at":           lambda x : timezone.localtime(),
            }
        )
        seed_space      = seeder.execute()
        space_id        = flatten(seed_space.values())[0]
        space           = Space.objects.get(id = space_id)

        random_number   = random.randint(1, len(reader))
        sub_image_list  = reader[random_number:random_number + 3]
        for sub_image_url in sub_image_list:
            SubImage.objects.create(space = space, image_url = sub_image_url)
        
        random_number   = random.randint(1, len(types))
        type_list       = types[random_number:random_number + 3]
        space.types.set(type_list)

        random_number   = random.randint(1, len(tags))
        tag_list        = tags[random_number:random_number + 4]
        for tag in tag_list:
            SpaceTag.objects.create(space = space, tag = tag)

        random_number   = random.randint(1, len(facilities))
        facility_lsit   = facilities[random_number : random_number + 6]
        for facility in facility_lsit:
            SpaceFacility.objects.create(space = space, facility = facility)

        random_number   = random.randint(1, len(breakdays))
        breakday_list   = breakdays[random_number: random_number + 1]
        for breakday in breakday_list:
            SpaceBreakday.objects.create(space = space, breakday = breakday)
            
        space.save()
        seeder.add_entity(
            DetailSpace,
            number,
            {
                "space":                  lambda x : space,
                "name":                   lambda x : random.choice(detail_name_list),
                "image":                  lambda x : reader[random.randint(0, image_length-1)],
                "min_reservation_time":   lambda x : random.randint(2, 5),
                "min_people":             lambda x : random.randint(1, 2),
                "max_people":             lambda x : random.randint(4, 10),
                "price":                  10000,
            }
        )
        seed_detail_space   = seeder.execute()
        detail_space_id     = flatten(seed_detail_space.values())[1]
        detail_space        = DetailSpace.objects.get(id = detail_space_id)
        
        random_number       = random.randint(1, len(detail_types))
        detail_type_list    = detail_types[random_number:random_number + 2]
        detail_space.detailtype_set.set(detail_type_list)

        random_number           = random.randint(1, len(detail_facilities))
        detail_facility_list    = detail_facilities[random_number:random_number + 6]
        detail_space.detailfacility_set.set(detail_facility_list)
        
        self.stdout.write(self.style.SUCCESS(f'spaces created {number}'))
        
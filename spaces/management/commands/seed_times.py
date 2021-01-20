import csv
import random
import bcrypt
from django_seed import Seed
from faker       import Faker

from django.contrib.admin.utils     import flatten
from django.core.management.base    import BaseCommand
from django.utils                   import timezone

from users.models   import Host
from spaces.models  import Space, DetailSpace, TimePrice

class Command(BaseCommand):
    help = "create time price"

    def add_arguments(self, parser):
        parser.add_argument("--number", type=int, default=1)

    def handle(self, *args, **options):
        number              = options.get("number")
        seeder              = Seed.seeder()
        detail_spaces       = DetailSpace.objects.all()
        fake                = Faker(["ko_KR"])
        seeder.add_entity(
            TimePrice,
            number,
            {   
                "detail_space":         lambda x : random.choice(detail_spaces),
                "price":                lambda x : random.randint(1, 10) * 1000,
                "people":               lambda x : random.randint(2, 5),
                "excess_price":         lambda x : random.randint(1, 5) * 1000,
                "created_at":           lambda x : timezone.now(),
                "updated_at":           lambda x : timezone.now()

            }
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'time price created {number}'))
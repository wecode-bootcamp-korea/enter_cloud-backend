import random

from django_seed                    import Seed
from django.core.management.base    import BaseCommand
from django.contrib.admin.utils     import timezone

from reviews.models      import Review
from users.models        import User
from spaces.models       import Space
from my_settings         import review_list


class Command(BaseCommand):
    help = "create reviews"

    def add_arguments(self, parser):
        parser.add_argument("--number", type=int, default=1)

    def handle(self, *args, **options):
        number  = options.get("number")
        spaces  = Space.objects.all()
        users   = User.objects.all()
        seeder  = Seed.seeder()
        seeder.add_entity(
            Review, 
            number,
            {
                "user":         lambda x : random.choice(users),
                "space":        lambda x : random.choice(spaces),
                "rating":       lambda x : random.randint(3, 5),
                "content":      lambda x : random.choice(review_list),
                "created_at":   lambda x : timezone.localtime(),
                "updated_at":   lambda x : timezone.localtime()
            }
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'review created {number}'))
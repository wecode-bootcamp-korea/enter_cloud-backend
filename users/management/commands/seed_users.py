import bcrypt

from django.core.management.base import BaseCommand
from django.contrib.admin.utils  import flatten

from users.models   import User, Host
from django_seed    import Seed
from faker          import Faker


class Command(BaseCommand):
    help = "create users"

    def add_arguments(self, parser):
        parser.add_argument("--number", type=int, default=1)

    def handle(self, *args, **options):
        number       = options.get("number")
        seeder       = Seed.seeder()
        fake         = Faker(["ko_KR"])
        users        = User.objects.all()
        max_count    = len(users)
        seeder.add_entity(
            User,
            number,
            {   
                "nickname":      lambda x : fake.name(),
                "email":         lambda x : seeder.faker.email(),
                "password":      bcrypt.hashpw("wecode123".encode(), bcrypt.gensalt()).decode(),
                "phone_number":  None,
                "avatar_image":  None
            }
        )
        seed_user      = seeder.execute()
        user_id        = flatten(seed_user.values())[0]
        user           = User.objects.get(id = user_id)

        Host.objects.create(user = user, host_avatar_image = None)
        self.stdout.write(self.style.SUCCESS(f'created user number : {number}' ))
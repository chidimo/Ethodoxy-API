from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from siteuser.models import CustomUser

class Command(BaseCommand):
    help = 'Create a superuser optionally passing an email and password'

    def add_arguments(self, parser):
        parser.add_argument('-email', type=str)
        parser.add_argument('-password', type=str)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Create superuser'))
        email = options['email'] if options['email'] else "admin@ethodoxy.net"
        password = options['password'] if options['password'] else "dwarfstar"

        try:
            su = CustomUser.objects.create_user(email=email, password=password)
            su.is_active = True
            su.save()
            self.stdout.write(self.style.SUCCESS(f'User {email} created successfully'))
        except IntegrityError:
            su = CustomUser.objects.get(email=email)
            self.stdout.write(self.style.ERROR(f'User {email} already exists'))
            pass

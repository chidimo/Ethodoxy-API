from django.core.management.base import BaseCommand, CommandError
from siteuser.models import SiteUser

class Command(BaseCommand):
    help = 'Reset all siteuser API quotas to default value'

    def add_arguments(self, parser):
        parser.add_argument('-quota', type=int)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start resetting api siteusers'))
        if options['quota']:
            quota = options['quota']
        else:
            quota = 1000
        siteusers = SiteUser.objects.all()
        for siteuser in siteusers:
            siteuser.quota = quota
            siteuser.used = 0
            siteuser.save(update_fields=['quota', 'used'])
        self.stdout.write(self.style.SUCCESS('Done resetting api siteusers'))

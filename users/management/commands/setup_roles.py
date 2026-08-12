from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Programmatically creates default RBAC groups for TruthGuard'

    def handle(self, *args, **kwargs):
        groups = ['Fact-Checker', 'TFGBV/Legal Expert', 'Field Reporter']
        
        for group_name in groups:
            # get_or_create ensures we don't accidentally duplicate groups
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created group: {group_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Group already exists: {group_name}'))
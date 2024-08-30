from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Create user groups passed as arguments."

    def add_arguments(self, parser):
        parser.add_argument(
            "groups", 
            nargs="+",
            type=str,
            help="List of groups to create."
        )
    
    def handle(self, *args, **options):
        groups = options.get("groups")

        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)

            if(created):
                self.stdout.write(self.style.SUCCESS(f"Successfully created group '%s'.") % group_name)
            else:
                self.stdout.write(self.style.WARNING(f"Group '%s' already exists.") % group_name)
            
        self.stdout.write(self.style.SUCCESS('Completed group creation process.'))
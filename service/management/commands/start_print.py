from service.utils import mailings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        mailings()
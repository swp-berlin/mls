from django.conf import settings
from django.core.management import BaseCommand, CommandError

import nltk

from mls.utils.embedding import download


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            nltk.download('punkt_tab', download_dir=settings.NLTK_DATA_DIR, raise_on_error=True)
            download(local_files_only=False)
        except ValueError as error:
            raise CommandError(f'{error}') from error

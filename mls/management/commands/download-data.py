from django.conf import settings
from django.core.management import BaseCommand, CommandError

import nltk

from fastembed import TextEmbedding


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            nltk.download('punkt_tab', download_dir=settings.NLTK_DATA_DIR, raise_on_error=True)
            TextEmbedding(settings.EMBEDDING_MODEL_NAME, cache_dir=settings.EMBEDDING_MODEL_CACHE_DIR)
        except ValueError as error:
            raise CommandError(f'{error}') from error

from functools import partial

from django.conf import settings

from pdfminer.high_level import extract_text

extract = partial(extract_text, maxpages=settings.EXTRACT_PDF_MAX_PAGES)

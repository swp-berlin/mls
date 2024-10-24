from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if settings.EMBEDDING_LIBRARY == 'fastembed':
    from .fastembed import download, embed, embed_query

elif settings.EMBEDDING_LIBRARY == 'sbert':
    from .sentence_transformers import download, embed, embed_query

else:
    raise ImproperlyConfigured(f'Embedding library {settings.EMBEDDING_LIBRARY} is not supported.')

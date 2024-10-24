from functools import lru_cache, partial
from typing import List

from django.conf import settings

from fastembed import TextEmbedding

from .chunking import get_chunks, avg


@lru_cache(maxsize=None)
def get_embedding(model_name, local_files_only=True):
    return TextEmbedding(
        model_name,
        local_files_only=local_files_only,
        cache_dir=settings.FASTEMBED_MODEL_CACHE_DIR,
    )


download = partial(get_embedding, settings.FASTEMBED_MODEL_NAME)


def get_tokenizer(embedding: TextEmbedding):
    return embedding.model.tokenizer.encode


def embed(text: str) -> List[float]:
    embedding = get_embedding(settings.FASTEMBED_MODEL_NAME)
    tokenizer = get_tokenizer(embedding)
    documents = get_chunks(text, tokenizer)
    embeddings = [*embedding.embed(documents)]

    return avg(documents, embeddings)


def embed_query(query: str) -> List[float]:
    [embedding] = get_embedding(settings.FASTEMBED_MODEL_NAME).query_embed([query])

    return embedding

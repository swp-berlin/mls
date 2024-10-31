from functools import lru_cache, partial
from typing import List

from django.conf import settings

from sentence_transformers import SentenceTransformer

from .chunking import get_chunks, avg


@lru_cache(maxsize=None)
def get_transformer(model_name, *, local_files_only=True):
    return SentenceTransformer(
        model_name,
        local_files_only=local_files_only,
        cache_folder=settings.SENTENCE_TRANSFORMERS_HOME,
    )


download = partial(get_transformer, settings.SENTENCE_TRANSFORMERS_MODEL_NAME)


def get_tokenizer(transformer: SentenceTransformer):
    encode = transformer.tokenizer.encode_plus

    def tokenizer(text: str):
        batch = encode(text, truncation=True)
        [encoded] = batch.encodings

        return encoded

    return tokenizer


def embed(text: str) -> List[float] | None:
    transformer = get_transformer(settings.SENTENCE_TRANSFORMERS_MODEL_NAME)
    tokenizer = get_tokenizer(transformer)
    sentences = get_chunks(text, tokenizer)

    if sentences:
        embeddings = transformer.encode(sentences)

        return avg(sentences, embeddings)


def embed_query(query: str) -> List[float]:
    [embedding] = get_transformer(settings.SENTENCE_TRANSFORMERS_MODEL_NAME).encode([query])

    return embedding

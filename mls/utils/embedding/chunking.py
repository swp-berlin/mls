import os

from typing import Callable, Iterator, List

import nltk
import numpy as np

from tokenizers import Encoding

Tokenizer = Callable[[str], Encoding]


def get_chunks(text: str, tokenize: Tokenizer):
    text = prepare_text(text)
    chunks = iter_chunks(text, tokenize)

    return list(chunks)


def prepare_text(text: str):
    return text.replace(f'-{os.linesep}', '')  # remove hyphenation


def iter_chunks(text: str, tokenize: Tokenizer) -> Iterator[str]:
    """
    Splits the text in chunks that are within the embedding's token limit preserving whole sentences when possible.
    """

    sentences = nltk.sent_tokenize(text)
    chunk = ''

    while sentences:
        sentence, *sentences = sentences

        if chunk:
            segment = f'{chunk} {sentence}'
        else:
            segment = sentence

        tokenized = tokenize(segment)

        if tokenized.overflowing:
            if not chunk:
                chunk, sentence = split_sentence(sentence, tokenize)
            sentences = [sentence, *sentences]
            yield chunk
            chunk = ''
        else:
            chunk = segment

    if chunk:
        yield chunk


def split_sentence(sentence: str, tokenize: Tokenizer):
    words = nltk.word_tokenize(sentence)
    chunk = ''

    while words:
        word, *words = words

        if chunk:
            segment = f'{chunk} {word}'
        else:
            segment = word

        tokenized = tokenize(segment)

        if tokenized.overflowing:
            if not chunk:
                # A word is too long for the token limit (should basically never happen).
                # We have no choice than split it.

                _, end = tokenized.offsets[-2]
                chunk, suffix = word[:end], word[end:]
                words = [suffix, *words]

            return chunk, ' '.join(words)

        chunk = segment


def avg(chunks: List[str], embeddings: List[np.array]) -> List[float]:
    """
    Averaging the chunks embedding vectors into a single vector using the method described by OpenAI:
    https://cookbook.openai.com/examples/embedding_long_inputs#2-chunking-the-input-text
    """

    weights = [*map(len, chunks)]
    average = np.average(embeddings, axis=0, weights=weights)
    average /= np.linalg.norm(average)

    return average.tolist()

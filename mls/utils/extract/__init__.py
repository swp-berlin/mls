from functools import partial
from typing import Callable, TypeAlias

from django.core.files.uploadedfile import UploadedFile, TemporaryUploadedFile

from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST
from sentry_sdk import capture_exception

from . import pdf

__all__ = [
    'Extractor',
    'ExtractException',
    'get_extractor',
]

Extractor = Callable[[UploadedFile], str]
MediaType: TypeAlias = str


class ExtractException(APIException):
    status_code = HTTP_400_BAD_REQUEST

    def __init__(self, error: Exception):
        APIException.__init__(self, f'{error}', code=error.__class__.__name__)


def extract(extractor: Extractor, obj: UploadedFile):
    try:
        return extractor(obj)
    except Exception as error:
        capture_exception(error)

        raise ExtractException(error) from error


def extract_plain(obj: UploadedFile):
    content: bytes = obj.read()

    return content.decode(obj.charset)


def extract_pdf(obj: UploadedFile):
    if isinstance(obj, TemporaryUploadedFile):
        return pdf.extract(obj.file.name)

    return pdf.extract(obj.file)


EXTRACTORS: dict[MediaType, Extractor] = {
    'text/plain': extract_plain,
    'application/pdf': extract_pdf,
}


def get_extractor(media_type: str) -> Extractor | None:
    if extractor := EXTRACTORS.get(media_type):
        return partial(extract, extractor)

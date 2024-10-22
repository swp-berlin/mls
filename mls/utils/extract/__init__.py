from typing import Callable, Optional, cast

from django.core.files.uploadedfile import UploadedFile

from .pdf import extract as extract_pdf

Extractor = Callable[[UploadedFile], str]


def extract_plain(obj: UploadedFile):
    content: bytes = obj.read()

    return content.decode(obj.charset)


extract_pdf = cast(Extractor, extract_pdf)


def get_extractor(media_type: str) -> Optional[Extractor]:
    match media_type:
        case 'text/plain':
            return extract_plain
        case 'application/pdf':
            return extract_pdf

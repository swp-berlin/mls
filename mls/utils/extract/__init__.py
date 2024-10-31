from typing import Callable, Optional

from django.core.files.uploadedfile import UploadedFile, TemporaryUploadedFile

from . import pdf

Extractor = Callable[[UploadedFile], str]


def extract_plain(obj: UploadedFile):
    content: bytes = obj.read()

    return content.decode(obj.charset)


def extract_pdf(obj: UploadedFile):
    if isinstance(obj, TemporaryUploadedFile):
        return pdf.extract(obj.file.name)

    return pdf.extract(obj.file)


def get_extractor(media_type: str) -> Optional[Extractor]:
    match media_type:
        case 'text/plain':
            return extract_plain
        case 'application/pdf':
            return extract_pdf

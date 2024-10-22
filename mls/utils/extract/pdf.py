from io import StringIO
from typing import BinaryIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

params = LAParams()
resources = PDFResourceManager(caching=True)


def extract(fp: BinaryIO, password: str = ''):
    output = StringIO()
    device = TextConverter(resources, output, laparams=params)
    interpreter = PDFPageInterpreter(resources, device)

    for page in PDFPage.get_pages(fp, password=password):
        interpreter.process_page(page)

    return output.getvalue()

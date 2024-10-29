from io import StringIO
from typing import BinaryIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdftypes import dict_value, resolve1

params = LAParams()
resources = PDFResourceManager(caching=True)


class FixedPDFPage(PDFPage):
    """
    See https://github.com/pdfminer/pdfminer.six/pull/1027
    """

    def __init__(self, doc, page, attrs, label):
        attrs = dict_value(attrs)

        if media_box := attrs.get('MediaBox'):
            attrs['MediaBox'] = resolve1(media_box)
        else:
            attrs['MediaBox'] = 0, 0, 612, 792  # US Letter

        PDFPage.__init__(self, doc, page, attrs, label)


def extract(fp: BinaryIO, password: str = ''):
    output = StringIO()
    device = TextConverter(resources, output, laparams=params)
    interpreter = PDFPageInterpreter(resources, device)

    for page in FixedPDFPage.get_pages(fp, password=password):
        interpreter.process_page(page)

    return output.getvalue()

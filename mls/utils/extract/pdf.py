from pdfminer.pdfpage import PDFPage
from pdfminer.pdftypes import dict_value, resolve1
from pdfminer import high_level


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


high_level.PDFPage = FixedPDFPage

extract = high_level.extract_text

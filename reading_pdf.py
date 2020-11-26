import PyPDF2 as pdf
from tika import parser
import fitz

def read_pdf(file):
    """PyPDF2 package is used to extract text from the pdf directly."""
    file = open(file,'rb')
    pdfreader = pdf.PdfFileReader()
    pdf_data = pdfreader.extractText()
    file.close()
    return pdf_data

def read_pdf2(file):
    """Tika package is also used to extract text from pdf directly"""
    """Java is required for it to run"""
    raw_text = parser.from_file(file)
    return raw_text['content']

def check_text_or_not(file):
    total_page_area = 0.0
    total_text_area = 0.0

    doc = fitz.open(file)

    for page_num, page in enumerate(doc):
        total_page_area = total_page_area + abs(page.rect)
        text_area = 0.0
        for b in page.getTextBlocks():
            r = fitz.Rect(b[:4])  # rectangle where block text appears
            text_area = text_area + abs(r)
        total_text_area = total_text_area + text_area
    doc.close()
    perc =  total_text_area / total_page_area
    if perc < 0.01:
        return True
    else:
        return False

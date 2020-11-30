from tika import parser
import subprocess

def read_pdf(file):
    """Tika package is also used to extract text from pdf directly"""
    """Java is required for it to run"""
    raw_text = parser.from_file(file)
    return raw_text['content']

def check_scanned_or_not(file_name):
    """subprocess is used to check whether the given document is scanned document or non scanned."""
    cmd = ['pdffonts', file_name]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=0, text=True, shell=False)
    out, err = proc.communicate()
    scanned = True
    for idx, line in enumerate(out.splitlines()):
        if idx == 2:
            scanned = False
    return scanned

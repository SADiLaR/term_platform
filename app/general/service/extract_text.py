from pypdf import PdfReader
from pypdf.errors import PdfStreamError


class GetTextError(Exception):
    pass


class GetTextFromPDF:
    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file

    def to_text(self):
        if self.uploaded_file:
            text_list = []
            # Read the PDF file and extract text
            try:
                reader = PdfReader(self.uploaded_file)
                for page in reader.pages:
                    text_list.append(page.extract_text())

                get_pdf_text = " ".join(text_list)

                return str(get_pdf_text)

            except PdfStreamError:
                raise GetTextError("The uploaded PDF file is corrupted or not fully downloaded.")

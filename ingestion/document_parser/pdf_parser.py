from pypdf import PdfReader


class PDFParser:

    def parse(self, pdf_path):

        reader = PdfReader(pdf_path)

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if text:
                pages.append({
                    "page": page_number,
                    "text": text
                })

        return pages
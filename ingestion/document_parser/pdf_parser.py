from pypdf import PdfReader


class PDFParser:

    def parse(self, pdf_path):

        reader = PdfReader(pdf_path)

        pages = []

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                pages.append(
                    {
                        "text": page_text
                    }
                )

        return pages
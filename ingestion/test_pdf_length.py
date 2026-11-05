from pypdf import PdfReader

reader = PdfReader("data/3gpp/TS38.300.pdf")

text = ""

for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
        text += page_text

print("Pages:", len(reader.pages))
print("Characters:", len(text))
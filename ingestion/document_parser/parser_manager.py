from .pdf_parser import PDFParser
from .json_parser import JSONParser
from .csv_parser import CSVParser


class ParserManager:

    def __init__(self):

        self.pdf_parser = PDFParser()
        self.json_parser = JSONParser()
        self.csv_parser = CSVParser()

    def parse(self, file_path):

        if file_path.endswith(".pdf"):
            return self.pdf_parser.parse(file_path)

        if file_path.endswith(".json"):
            return self.json_parser.parse(file_path)

        if file_path.endswith(".csv"):
            return self.csv_parser.parse(file_path)

        raise Exception("Unsupported file format")
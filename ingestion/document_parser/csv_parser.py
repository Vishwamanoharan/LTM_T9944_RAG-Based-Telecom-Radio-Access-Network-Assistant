import pandas as pd

class CSVParser:

    def parse(self, csv_path):

        df = pd.read_csv(csv_path)

        return df.to_dict(orient="records")
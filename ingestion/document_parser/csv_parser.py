import pandas as pd


class CSVParser:

    def parse(self, csv_path):

        dataframe = pd.read_csv(csv_path)

        return dataframe.to_dict(
            orient="records"
        )
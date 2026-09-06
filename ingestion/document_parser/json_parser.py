import json


class JSONParser:

    def parse(self, json_path):

        with open(
            json_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)
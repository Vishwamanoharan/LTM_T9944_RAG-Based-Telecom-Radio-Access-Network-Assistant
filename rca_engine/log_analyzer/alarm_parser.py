import json
import os


class AlarmParser:

    def __init__(self, incidents_path="data/telelogs/incidents.json"):
        self.incidents_path = incidents_path
        self.incidents = self._load_incidents()

    def _load_incidents(self):
        if not os.path.exists(self.incidents_path):
            return []

        with open(self.incidents_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []

        return data

    def get_all_incidents(self):
        return self.incidents

    def get_all_events(self):
        events = set()

        for incident in self.incidents:
            event = incident.get("incident")

            if event:
                events.add(event)

        return sorted(events)

    def get_incidents_by_event(self, event):
        if not event:
            return []

        target = str(event).strip().lower()

        return [
            incident
            for incident in self.incidents
            if str(incident.get("incident", "")).strip().lower() == target
        ]

    def get_incidents_by_tower(self, tower):
        if not tower:
            return []

        target = str(tower).strip().lower()

        return [
            incident
            for incident in self.incidents
            if str(incident.get("tower", "")).strip().lower() == target
        ]

    def count_incidents(self):
        return len(self.incidents)
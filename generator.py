from database import Database
from template import Template


class Generator:
    def __init__(self, template, database):
        self.template = template
        self.db = database.get_connection()
        self.record = None

    def generate_header(self):
        pass

    def generate_records(self):
        for section in self.template.get_data_sections():
            print(section)

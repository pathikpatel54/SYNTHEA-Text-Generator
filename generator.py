from database import Database
from template import Template


class Generator:
    def __init__(self, template, database):
        self.template = template
        self.db = database.get_connection()
        self.tables = []

    def generate_header(self):
        for item in self.template.get_header_section():
            section_name, value = item
            self.template.get_template(section_name)

    def generate_records(self):
        for section in self.template.get_data_sections():
            section_name, value = section
            table_name = self.template.get_table_name(section_name)
            sub_sections = self.template.get_subsections(section_name)
            for sub_section in sub_sections.items():
                print(sub_section[0])
            print(table_name)

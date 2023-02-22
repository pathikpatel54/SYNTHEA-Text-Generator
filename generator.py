from operator import itemgetter
from database import Database
from template import Template


class Generator:
    def __init__(self, template, database):
        self.template = template
        self.db = database
        self.section_records = {section[0]: list(self.db.get_table_records(section[1].get("table")))
                                for section in self.template.get_data_sections()[1:]}

    def generate_header(self):
        pass

    def generate_patient_record(self):
        main_table_name = self.template.get_data_sections(
        )[self.template.get_main_table_index()][1]["table"]
        main_records = self.db.get_table_records(main_table_name)
        for section_name, section_records in self.section_records.items():
            join_column = self.template.get_join(section_name)[0]
            for main_record in main_records:
                yield {**main_record, section_name: [sr for sr in section_records if sr.get(join_column) == main_record.get(join_column)]}

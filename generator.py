from datetime import datetime
import random
import re
from dateutil.relativedelta import relativedelta


class Generator:
    def __init__(self, template, database):
        self.template = template
        self.db = database
        self.section_records = {section[0]: list(self.db.get_table_records(section[1].get("table")))
                                for section in self.template.get_data_sections()[1:]}

    def generate_header(self):
        header = self.template.get_header_template()[0]
        for match in re.findall("{:([A-Z_]+):}", header):
            field_value = self.template.get_var(match)
            header = header.replace("{:" + match + ":}", field_value)
        return header + self.template.get_header_template()[random.randrange(1, len(self.template.get_header_template()))]

    def generate_footer(self):
        return (self.template.get_footer_template())[0]

    def generate_patient_record(self):
        main_table_name = self.template.get_data_sections(
        )[self.template.get_main_table_index()][1]["table"]
        main_records = self.db.get_table_records(main_table_name)
        for section_name, section_records in self.section_records.items():
            join_column = self.template.get_join(section_name)[0]
            for main_record in main_records:
                yield {**main_record, section_name: [sr for sr in section_records if sr.get(join_column) == main_record.get(join_column)]}, join_column

    def generate_patient_string(self, record):
        sections = self.template.get_sections_list()
        returnstring = ""
        section_title = ""
        for section, sub_name, value in sections:
            section_title, conditions = value.get(
                "title", random.choice(self.template.get_section_title(section))), value.get("when", [])
            sub_template = self.template.get_template(sub_name)
            section_details = record.get(section, record)
            if self.check_conditions(section_details, conditions) == False:
                continue
            template_list = [sub_template] if isinstance(
                sub_template, list) else sub_template.values()
            returnstring += section_title
            for template in template_list:
                sentence = template[random.randrange(len(template))]
                returnstring += self.fill_template(sentence, section_details)

        return returnstring

    def fill_template(self, template, values):
        values = values if isinstance(values, list) else [values]
        result = "" if re.findall("{:([A-Z_]+):}", template) else template
        for value in values:
            mod_template = template
            for match in re.findall("{:([A-Z_]+):}", mod_template):
                field_value = value.get(match)
                if match == "AGE":
                    field_value = str(relativedelta(
                        datetime.now(), value.get("BIRTHDATE")).years)
                if field_value is not None:
                    field_value = field_value.strftime(
                        '%m/%d/%Y') if isinstance(field_value, datetime) else field_value
                    field_value = self.template.get_mappings().get(
                        match, {}).get(field_value, field_value)
                    mod_template = mod_template.replace(
                        "{:" + match + ":}", field_value)
            match = re.findall("{:([A-Z_]+):}", mod_template)
            mod_template = "" if len(match) > 0 else mod_template
            if mod_template not in result:
                result += mod_template
        return result

    def generate_patient_offset(self):
        main_table_name = self.template.get_data_sections(
        )[self.template.get_main_table_index()][1]["table"]
        main_records = self.db.get_table_records(main_table_name)
        for section_name, section_records in self.section_records.items():
            join_column = self.template.get_join(section_name)[0]
            for main_record in main_records:
                yield {**main_record, section_name: [sr for sr in section_records if sr.get(join_column) == main_record.get(join_column)]}, join_column

    def check_conditions(self, record, conditions):
        if not conditions:
            return True
        field, comparator, val = conditions
        if (match := re.findall("{:([A-Z]+):}", field)) == [] and field == "count":
            count = len(record)
            if comparator == "EQ" and count != val or comparator == "GT" and count <= val:
                return False
        elif record[match[0]] != val:
            return False
        return True

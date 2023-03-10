from datetime import datetime
import random
import re
from dateutil.relativedelta import relativedelta


class Generator:
    def __init__(self, template, database):
        self.template = template
        self.db = database
        self.section_records = self.generate_section_records()

    def generate_section_records(self):
        data_sections = self.template.get_data_sections()[1:]
        section_records = {}

        for section in data_sections:
            table_name = section[1].get("table")
            table_records = list(self.db.get_table_records(table_name))
            section_name = section[0]
            section_records[section_name] = table_records
        return section_records

    def generate_header(self):
        header = self.template.get_header_template()[0]
        for match in re.findall("{:([A-Z_]+):}", header):
            field_value = self.template.get_var(match)
            header = header.replace("{:" + match + ":}", field_value)
        return header + self.template.get_header_template()[random.randrange(1, len(self.template.get_header_template()))]

    def generate_footer(self):
        return (self.template.get_footer_template())[0]

    def generate_patient_record(self):
        main_table_name = self.template.get_main_table_name()
        main_section_name = self.template.get_main_section_name()
        main_join_column = self.template.get_join(main_section_name)[0]
        main_records = self.db.get_table_records(main_table_name)
        for main_record in main_records:
            for section_name, section_records in self.section_records.items():
                main_record[section_name] = []
                join_column = self.template.get_join(section_name)[0]
                for section_record in section_records:
                    if main_record[main_join_column] == section_record[join_column]:
                        main_record[section_name].append(section_record)
            yield main_record, main_join_column

    def generate_patient_string(self, record):
        sections = self.template.get_sections_list()
        result = ""
        offsets = {}
        for section, sub_name, value in sections:
            section_title, conditions = value.get(
                "title", random.choice(self.template.get_section_title(section))), value.get("when", [])
            sub_template = self.template.get_template(sub_name)
            section_details = record.get(section, record)
            if self.check_conditions(section_details, conditions) == False:
                continue
            template_list = [sub_template] if isinstance(
                sub_template, list) else sub_template.values()
            result += section_title
            line = result.count("\n") + 1
            wordscount = len(result)
            for template in template_list:
                sentence = template[random.randrange(len(template))]
                if isinstance(sentence, dict):
                    sentence = sentence.get(
                        "part_1")[0] + sentence.get("part_2")[0]
                returns = self.fill_template(sentence,
                                             section_details, section, wordscount)

                offset = self.adjust_patient_offset(result, returns[1])
                if returns[1] == {} and returns[0] != "" and section_details == []:
                    offset = {section: {
                        "offset": str(wordscount),
                        "length": len(returns[0])
                    }}
                offsets.update(offset)
                result += returns[0]
        return result, offsets

    def fill_template(self, template, values, section, wordscount):
        flag = 1 if isinstance(values, list) else 0
        values = values if isinstance(values, list) else [values]
        result = "" if re.findall("{:([A-Z_]+):}", template) else template
        offset_object = {}
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
                    column = mod_template.index("{:" + match + ":}")
                    offset = {"offset": str(
                        column + wordscount), "length": len(field_value)}
                    if flag == 0:
                        offset_object[match] = offset
                    mod_template = mod_template.replace(
                        "{:" + match + ":}", field_value)
            match = re.findall("{:([A-Z_]+):}", mod_template)
            mod_template = "" if len(match) > 0 else mod_template
            if mod_template not in result:
                result += mod_template
            if flag == 1:
                offset = {"offset": str(wordscount),
                          "length": len(mod_template)}
                if offset_object.get(section) is None:
                    offset_object[section] = offset
                else:
                    if isinstance(offset_object[section], dict):
                        offset_object[section] = [offset_object[section]]
                    offset_object[section].append(offset)
        return result, offset_object

    def adjust_patient_offset(self, result, offset):
        sentences = result.split("\n")
        if len(sentences) > 0:
            count = [len(sentences[-1])]
            for key, value in offset.items():
                if isinstance(value, dict) and value.get("offset") is not None:
                    original_offset = value.get("offset")
                    new_offset = int(original_offset) + len(sentences[-1])
                    offset[key]["offset"] = str(new_offset)
                if isinstance(value, list):
                    offset[key] = list(
                        map(lambda p: self.map_offsets(p, count), value))
        return offset

    def map_offsets(self, value, count):
        original_offset = value.get("offset")
        original_length = int(value.get("length"))
        new_offset = int(original_offset) + count[0]
        value["offset"] = str(new_offset)
        count[0] += original_length
        return value

    def adjust_lineoffsets(self, output_string, offsets):
        words = len(output_string)
        for key, value in offsets.items():
            if isinstance(value, dict) and value.get("offset") is not None:
                original_offset = value.get("offset")
                new_offset = int(original_offset) + words
                offsets[key]["offset"] = str(new_offset)
            if isinstance(value, list):
                offsets[key] = list(
                    map(lambda p: self.map_lineoffsets(p, words), value))
        return offsets

    def map_lineoffsets(self, value, words):
        original_offset = value.get("offset")
        new_offset = int(original_offset) + words
        value["offset"] = str(new_offset)
        return value

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

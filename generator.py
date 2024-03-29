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
            wordscount = len(result)
            for template in template_list:
                sentence = template[random.randrange(len(template))]
                returns = self.fill_template(sentence,
                                             section_details, section, wordscount)

                offset = self.adjust_patient_offset(result, returns[1])
                if returns[1] == {} and returns[0] != "" and section_details == []:
                    offset = {section: {
                        "offset": wordscount,
                        "length": len(returns[0])
                    }}
                if offsets.get(section) is None or isinstance(offsets.get(section), list):
                    offsets.update(offset)
                else:
                    offsets[section]["length"] = offsets[section]["length"] + \
                        len(returns[0])
                result += returns[0]
        return result, offsets

    def fill_template(self, templates, values, section, wordscount):
        flag = 1 if isinstance(values, list) else 0
        values = values if isinstance(values, list) else [values]
        final_result = templates if isinstance(templates, str) and not re.findall(
            "{:([A-Z_]+):}", templates) else ""
        templates = [templates] if isinstance(
            templates, str) else templates.values()
        offset_object = {}
        for value in values:
            final_template = ""
            for template in templates:
                template = template if isinstance(
                    template, str) else template[random.randrange(len(template))]
                result = "" if re.findall(
                    "{:([A-Z_]+):}", template) else template
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
                        offset = {"offset": column + wordscount,
                                  "length": len(field_value),
                                  "value": field_value
                                  }
                        if flag == 0:
                            offset_object[match] = offset
                        mod_template = mod_template.replace(
                            "{:" + match + ":}", field_value)
                match = re.findall("{:([A-Z_]+):}", mod_template)
                mod_template = "" if len(match) > 0 else mod_template
                final_template += mod_template
            if final_template not in result:
                result += final_template
            if flag == 1:
                offset = {"offset": wordscount,
                          "length": len(final_template)}
                if offset_object.get(section) is None:
                    offset_object[section] = offset
                else:
                    if isinstance(offset_object[section], dict):
                        offset_object[section] = [offset_object[section]]
                    offset_object[section].append(offset)
            if result not in final_result:
                final_result += result
            if len(final_result) > 0 and final_result[-1] == ",":
                final_result = final_result[:-1] + "."
        return final_result, offset_object

    def adjust_patient_offset(self, result, offset):
        sentences = result.split("\n")
        if len(sentences) > 0:
            count = [len(sentences[-1])]
            for key, value in offset.items():
                if isinstance(value, dict) and value.get("offset") is not None:
                    original_offset = value.get("offset")
                    new_offset = int(original_offset) + len(sentences[-1])
                    offset[key]["offset"] = new_offset
                if isinstance(value, list):
                    offset[key] = list(
                        map(lambda p: self.map_offsets(p, count), value))
        return offset

    def map_offsets(self, value, count):
        original_offset = value.get("offset")
        original_length = int(value.get("length"))
        new_offset = int(original_offset) + count[0]
        value["offset"] = new_offset
        count[0] += original_length
        return value

    def adjust_lineoffsets(self, output_string, offsets):
        words = len(output_string)
        for key, value in offsets.items():
            if isinstance(value, dict) and value.get("offset") is not None:
                original_offset = value.get("offset")
                new_offset = int(original_offset) + words
                offsets[key]["offset"] = new_offset
            if isinstance(value, list):
                offsets[key] = list(
                    map(lambda p: self.map_lineoffsets(p, words), value))
        return offsets

    def map_lineoffsets(self, value, words):
        original_offset = value.get("offset")
        new_offset = int(original_offset) + words
        value["offset"] = new_offset
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

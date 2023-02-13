import json


class Template:
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            self.json_data = json.load(f)

    def get_vars(self):
        return self.json_data['vars']

    def get_section(self, section_name):
        return self.json_data['sections'].get(section_name, {})

    def get_table_name(self, section_name):
        return self.get_section(section_name).get('table')

    def get_table_columns(self, section_name):
        return self.get_section(section_name).get('columns')

    def get_join(self, section_name):
        return self.get_section(section_name).get('join')

    def get_subsections(self, section_name):
        return self.get_section(section_name).get('sections', {})

    def get_templates(self):
        return self.json_data.get('templates', {})

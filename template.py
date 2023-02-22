import json

class Template:
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            self.json_data = json.load(f)

    def get_var(self, var_name) -> dict:
        return self.json_data.get("vars", {}).get(var_name)

    def get_connection(self, var_name) -> dict:
        return self.json_data.get("connection", {}).get(var_name)

    def get_template(self, template_name) -> dict:
        return self.json_data.get("templates", {}).get(template_name)

    def get_sections_items(self):
        return self.json_data.get("main", {}).items()

    def get_header_section(self):
        return list(filter(lambda x: "HEADER" in x[0], self.get_sections_items()))

    def get_footer_section(self):
        return list(filter(lambda x: "FOOTER" in x[0], self.get_sections_items()))

    def get_data_sections(self):
        return list(filter(lambda x: x[1].get("table", False) != False, self.get_sections_items()))

    def get_section(self, section_name):
        return self.json_data.get("main", {}).get(section_name)

    def get_table_name(self, section_name):
        return self.get_section(section_name).get('table')

    def get_table_columns(self, section_name):
        return self.get_section(section_name).get('columns')

    def get_title(self, section_name):
        return self.get_section(section_name).get('title')

    def get_join(self, section_name):
        return self.get_section(section_name).get('join')
    
    def get_subsections(self, section_name):
        return self.get_section(section_name).get('sections')

    def get_templates(self):
        return self.json_data.get('templates', {})

    def get_template(self, section_name):
        return self.json_data.get('templates', {}).get(section_name, {})

    def get_main_table_index(self):
        for section in range(len(self.get_data_sections())):
            section_name = self.get_data_sections()[section][0]
            if not self.json_data.get('sections', {}).get(section_name, {}).get("join"):
                return section

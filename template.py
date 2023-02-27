import json


class Template:
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            self.json_data = json.load(f)

    def get_vars(self) -> dict:
        return self.json_data.get("vars", {}).items()

    def get_var(self, var_name) -> dict:
        return self.json_data.get("vars", {}).get(var_name)

    def get_section_title(self, section_name) -> dict:
        title = self.get_title(section_name)
        if self.get_template(title) == [] or self.get_template(title) is None:
            return [""]
        return self.get_template(title)

    def get_mappings(self) -> dict:
        return self.json_data.get("mappings", {})

    def get_connection(self, var_name) -> dict:
        return self.json_data.get("connection", {}).get(var_name)

    def get_templates(self):
        return self.json_data.get('templates', {})

    def get_template(self, section_name) -> dict:
        return self.json_data.get("templates", {}).get(section_name)

    def get_header_template(self):
        return self.json_data.get("templates", {}).get(self.get_header_section()[0][0])

    def get_footer_template(self):
        return self.json_data.get("templates", {}).get(self.get_footer_section()[0][0])

    def get_sections_list(self):
        return [(section[0], item, value) for section in self.get_data_sections() for item, value in self.get_subsections(section[0]).items()]

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

    def get_main_table_index(self):
        return next((i for i, section in enumerate(self.get_data_sections()) if not self.json_data.get('sections', {}).get(section[0], {}).get("join")), None)

    def get_main_section_name(self):
        return self.get_data_sections()[self.get_main_table_index()][0]

    def get_main_table_name(self):
        return self.get_data_sections()[self.get_main_table_index()][1]["table"]

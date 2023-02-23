import json
from template import Template
from database import Database
from generator import Generator

inputFile = open("./input/templates.json")
inputTemplate = json.load(inputFile)


def main():
    template = Template("./input/templates.json")

    db_host, db_sid = template.get_connection(
        "DBHOST"), template.get_connection("DBSID")
    database = Database(db_host, db_sid)
    generator = Generator(template, database)

    for patient_record, join_column in generator.generate_patient_record():
        output_string = generator.generate_header()
        output_string += generator.generate_patient_string(
            patient_record)
        output_string += generator.generate_footer()
        writeToOutput(output_string, patient_record.get(join_column))


def writeToOutput(string, name):
    outputFile = open(f"./output/{name}.txt", "w")
    outputFile.write(string)
    outputFile.close()


main()

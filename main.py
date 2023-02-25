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

        output, offsets = generator.generate_patient_string(
            patient_record)
        offsets = generator.adjust_lineoffsets(output_string, offsets)
        output_string += output
        output_string += generator.generate_footer()
        writeToOutput(output_string, patient_record.get(
            join_column), json.dumps(offsets, indent=4))


def writeToOutput(string, name, offsets):
    outputFile = open(f"./output/{name}.txt", "w")
    outputFile.write(string)
    outputFile.close()
    offsetFile = open(f"./output/{name}.json", "w")
    offsetFile.write(offsets)
    offsetFile.close()


main()

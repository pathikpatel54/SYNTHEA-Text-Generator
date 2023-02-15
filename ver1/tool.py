from datetime import datetime
import json
import oracledb
from dateutil.relativedelta import relativedelta
from random import randrange


def main():
    f = open("./input/templates.json")
    templates = json.load(f)

    db = """(DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = oracle2.cci.drexel.edu)(PORT = 1521))
    (CONNECT_DATA =
        (SID = ORCL)
    ))"""

    connection = oracledb.connect(
        user="pap325", password="ftSFH8N3t8S", dsn=db)
    patientAllergies = getPatientAllergies(connection.cursor())
    patients = getPatients(connection.cursor())

    for patient in patients:
        for allergies in patientAllergies:
            if patient["PATIENT_ID"] == allergies["PATIENT_ID"]:
                patient["ALLERGIES"] = patient.get("ALLERGIES", [])
                patient["ALLERGIES"].append(allergies)
        generate_patient_file(patient, templates)


def generate_patient_file(patient, templates):
    header = generate_header(templates)
    patientId = patient["PATIENT_ID"]
    firstName = patient["FIRST"]
    lastName = patient["LAST"]
    age = relativedelta(datetime.now(), patient["BIRTHDATE"]).years
    gender = "female" if patient["GENDER"] == "F" else "male"
    address = patient["ADDRESS"] + ", " + patient["CITY"]
    marital = "married" if patient["MARITAL"] == "M" else "single" if patient["MARITAL"] == "S" else "unknown"
    race = patient["RACE"].capitalize()
    allergies = patient.get("ALLERGIES", [])

    outputFile = open(f"./output/{patientId}.txt", "a")
    patientString = ''
    patientString += templates["demographicsTemplates"][randrange(10)].replace(
        "[Patient Name]", firstName + " " + lastName)
    patientString = patientString.replace("[Age]", str(age))
    patientString = patientString.replace("[Gender]", gender)
    patientString = patientString.replace("[Address]", address)
    patientString = patientString.replace("[Marital Status]", marital)
    patientString = patientString.replace("[Race]", race)

    outputFile.write(patientString + allergiesString)
    outputFile.close()


def generate_header(templates):
    header = templates["templates"]["DOCUMENT_HEADER"]


def generate_allergies()


def getPatientAllergies(allergy_cursor):
    allergy_cursor.execute("SELECT * FROM synthea_patient_allergy")
    a_columns = [col[0] for col in allergy_cursor.description]
    allergy_cursor.rowfactory = lambda *args: dict(zip(a_columns, args))
    return allergy_cursor.fetchall()


def getPatients(patient_cursor):
    patient_cursor.execute("SELECT * FROM synthea_patient")
    p_columns = [col[0] for col in patient_cursor.description]
    patient_cursor.rowfactory = lambda *args: dict(zip(p_columns, args))
    for patient in patient_cursor:
        yield patient


main()

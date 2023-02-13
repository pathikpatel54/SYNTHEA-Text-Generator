from datetime import datetime
import json
import re
import oracledb
from random import randrange
from dateutil.relativedelta import relativedelta
from template import Template

inputFile = open("./input/templates.json")
inputTemplate = json.load(inputFile)


def main():
    generateSections(connectDatabase())


def connectDatabase():
    VARS = inputTemplate['vars']
    db = f"""(DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = {VARS['DBHOST']})(PORT = 1521))
    (CONNECT_DATA =
        (SID = {VARS["DBSID"]})
    ))"""
    connection = oracledb.connect(
        user="pap325", password="ftSFH8N3t8S", dsn=db)
    return connection


def getTable(mainCursor, sectionName):
    tableName = inputTemplate.get('sections', {}).get(
        sectionName, {}).get('table')
    if tableName is None:
        print("Input file not structured correctly")
        return
    mainCursor.execute(
        f"SELECT * FROM {tableName}")
    columns = [col[0] for col in mainCursor.description]
    mainCursor.rowfactory = lambda *args: dict(zip(columns, args))
    for record in mainCursor:
        yield record


def generateSections(database):
    items = inputTemplate['sections'].items()
    sections = []
    for sectionName, value in items:
        if "HEADER" in sectionName:
            # generateHeader(cursor, sectionName)
            pass
        elif value.get("table", False):
            sections.append(sectionName)
    generateRecords(database, sections)


def getMainTableIndex(sections):
    for section in range(len(sections)):
        if not inputTemplate['sections'].get(sections[section], {}).get("join"):
            return section


def generateRecords(database, sections):
    mainTableIndex = getMainTableIndex(sections)
    sectionTableRecords = {
        sections[section]: list(getTable(database.cursor(), sections[section])) for section in range(1, len(sections))}
    mainTableRecords = getTable(database.cursor(), sections[mainTableIndex])

    for section in sectionTableRecords.keys():
        join = inputTemplate.get("sections", {}).get(
            section, {}).get("join")[0]
        for mainTableRecord in mainTableRecords:
            mainTableRecord[section] = []
            for sectionRecord in sectionTableRecords[section]:
                if sectionRecord.get(join) == mainTableRecord.get(join):
                    mainTableRecord[section].append(sectionRecord)
            writeToOutput(getTemplate(mainTableRecord, sections), mainTableRecord[join])
            


def getTemplate(record, sections):
    sections = getSectionsList(sections)
    returnstring = ""
    for section, sub, value in sections:
        conditions = value.get("when", [])
        template = inputTemplate.get("templates", {}).get(sub)
        sectionDetails = record if record.get(
            section) is None else record.get(section)

        if len(sectionDetails) == 0:
            continue

        if checkConditions(sectionDetails, conditions) == False:
            continue

        sentence_list = [template] if isinstance(
            template, list) else template.values()
        for templateValue in sentence_list:
            sentence = templateValue[randrange(len(templateValue))]
            returnstring += fillTemplateValues(sentence, sectionDetails)
    return returnstring


def checkConditions(record, conditions):
    if len(conditions) == 0:
        return True
    field, comparator, val = conditions
    match = re.findall("{:([A-Z]+):}", field)
    if match == [] and field == "count":
        count = len(record)
        if comparator == "EQ":
            if count != val:
                return False
        if comparator == "GT":
            if count <= val:
                return False
    else:
        if record[match[0]] != val:
            return False

    return True


def getSectionsList(sections):
    sectionsList = []
    for section in sections:
        sectionObj = inputTemplate.get("sections").get(section).get("sections")
        for item, value in sectionObj.items():
            sectionsList.append((section, item, value))
    return sectionsList


def fillTemplateValues(template, values):
    values = values if isinstance(values, list) else [values]
    returnString = ""
    for value in values:
        modtemplate = template
        for match in re.findall("{:([A-Z_]+):}", modtemplate):
            fieldValue = value.get(match)

            if match == "AGE":
                age = str(relativedelta(datetime.now(),
                                        value.get("BIRTHDATE")).years)
                modtemplate = modtemplate.replace(
                    "{:" + match + ":}", age)
            if fieldValue is not None:
                fieldValue = fieldValue.strftime(
                    '%m/%d/%Y') if isinstance(fieldValue, datetime) else fieldValue
                if match in inputTemplate.get("vars").keys():
                    fieldValue = inputTemplate.get(
                        "vars").get(match).get(fieldValue)
                modtemplate = modtemplate.replace(
                    "{:" + match + ":}", fieldValue)

        match = re.findall("{:([A-Z_]+):}", modtemplate)
        modtemplate = "" if len(match) > 0 else modtemplate
        if modtemplate not in returnString:
            returnString += modtemplate

    return returnString

def writeToOutput(string, name):
    outputFile = open(f"./output/{name}", "w")
    outputFile.write(string)
    outputFile.close()

main()

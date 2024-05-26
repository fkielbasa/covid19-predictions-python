import json

from CovidCase import CovidCase
from CovidData import CovidData


def getData():
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    lista = []

    for entry in data:
        country = entry["country"]
        cases = entry["cases"]
        # print(f"Country: {country}")
        for date, case_info in cases.items():
            # print(f"Date: {date}, Total: {case_info['total']}, New: {case_info['new']}")
            lista += [CovidCase(date, case_info['total'], case_info['new'])]
        covidData = CovidData(country, "", lista)
        return covidData

    return None

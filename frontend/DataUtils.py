import json
import datetime

def load_countries():
    try:
        with open("data/Countries.json", "r", encoding="utf-8") as f:
            countries_data = json.load(f)
            return countries_data["countries"]
    except FileNotFoundError:
        return []

def filter_data_by_dates(data, start_date, end_date):
    filtered_cases = {date: details for date, details in data[0]['cases'].items() if
                      start_date <= datetime.datetime.strptime(date, '%Y-%m-%d') <= end_date}
    return [{'country': data[0]['country'], 'region': data[0]['region'], 'cases': filtered_cases}]

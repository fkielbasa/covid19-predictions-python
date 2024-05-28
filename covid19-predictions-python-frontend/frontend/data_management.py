import json
import requests
def load_data(country):
    # Definiujemy kraj, dla którego chcemy pobrać dane
    '''country = 'Spain'''''
    api_url = 'https://api.api-ninjas.com/v1/covid19?country={}'.format(country)

    # Wykonujemy zapytanie do API
    response = requests.get(api_url, headers={'X-Api-Key': 'ysJcUE/TeWo6yRbktNfNtw==1iEmOIxBoXTUg5PP'})

    data = response.json()

    return  data
    '''
    filename = f'data/CovidData{country}.json'
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        # Zakładam, że dane są listą i filtrujemy po kluczu 'country' każdego elementu w liście
        filtered_data = [item for item in data if item['country'] == country]
        return filtered_data
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    except KeyError:
        print("Invalid data format in the file.")
        return []
'''
def load_countries():
    with open('data/Countries.json', 'r') as file:
        data = json.load(file)
    return data['countries']
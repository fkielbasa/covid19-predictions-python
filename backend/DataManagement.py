import json
import requests
def load_data(country):
    '''country = 'Spain'''''
    api_url = 'https://api.api-ninjas.com/v1/covid19?country={}'.format(country)
    response = requests.get(api_url, headers={'X-Api-Key': 'ysJcUE/TeWo6yRbktNfNtw==1iEmOIxBoXTUg5PP'})

    data = response.json()

    return  data
def load_countries():
    with open('../frontend/data/Countries.json', 'r') as file:
        data = json.load(file)
    return data['countries']
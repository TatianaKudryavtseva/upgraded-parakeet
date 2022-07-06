import environ
import requests
import json
from pprint import pprint


env = environ.Env()
environ.Env.read_env()

''' NASA API '''
''' Astronomy Picture of the Day '''

url = "https://api.nasa.gov/planetary/apod"

params = {'api_key': env('SECRET_KEY'),
          'start_date': '2022-07-01',
          'end_date': '2022-07-03'}

response = requests.request("GET", url, params=params)
response = response.json()

with open("nasa_file.json", "w") as write_file:
    json.dump(response, write_file)

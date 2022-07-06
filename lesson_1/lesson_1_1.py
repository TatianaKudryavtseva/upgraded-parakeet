import requests
from pprint import pprint
import json


username = 'TatianaKudryavtseva'
url = 'https://api.github.com/users/'+username+'/repos'
response = requests.get(url)
lesson = response.json()

with open("response_file_2.json", "w") as write_file:
    json.dump(lesson, write_file)

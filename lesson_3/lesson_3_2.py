from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017')
db = client['user1007']
jobs = db.jobs


def get_vacancy_with_salary_more_then(number):
    for item in jobs.find({'$or': [
        {'salary_min': {'$gt': number}},
        {'salary_max': {'$gt': number}}
    ]}):
        pprint(item)


get_vacancy_with_salary_more_then(120000)

client.close()

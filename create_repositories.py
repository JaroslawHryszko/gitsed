# loading libraries
from pymongo import MongoClient
import json, csv, pymongo, time, urllib, sys

# opening config file
with open('config.json') as json_data_file:
    config = json.load(json_data_file)

# opening connection with database
client = MongoClient(config['database']['server'])
db = client.github

csv_file = '/Users/avenuecode/Downloads/DataSet/J_repository.csv'
with open(csv_file, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        print row[3]
        # repositories
        data = {
            "repository_id": int(row[0]),
            "name": row[1],
            "description": row[2],
            "url": row[4],
            "create_date": row[5],
            "end_date": row[6],
            "duration_days": int(row[7]),
            "number_add_lines": int(row[8]),
            "number_del_lines": int(row[9]),
            "number_commits": int(row[10]),
            "number_commiters": int(row[11])
        }
        if int(row[3]) == 1:
            data['programming_language'] = 'javascript'
        elif int(row[3]) == 2:
            data['programming_language'] = 'ruby'
        else:
            data['programming_language'] = 'java'
        db.repositories.insert(data)
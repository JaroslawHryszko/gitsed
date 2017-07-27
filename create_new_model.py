# loading libraries
from pymongo import MongoClient
import json, csv, pymongo, time, urllib, sys

# opening config file
with open('config.json') as json_data_file:
    config = json.load(json_data_file)

# opening connection with database
client = MongoClient(config['database']['server'])
db = client.github

csv_file = '/Users/avenuecode/Downloads/DataSet/J_developers_social_network.csv'
with open(csv_file, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        print row[8]
        devs = []
        user_1 = db.users.find({ 'gitsed_id': int(row[1])}, no_cursor_timeout=True)
        user_2 = db.users.find({ 'gitsed_id': int(row[2])}, no_cursor_timeout=True)
        for user in user_1:
            devs.append({'_id': user['_id'], 'login': user['login']})
        for user in user_2:
            devs.append({'_id': user['_id'], 'login': user['login']})
        data = {
            "repository_id": int(row[0]),
            'developers': devs,
            'begin_contribute_date': row[3],
            'end_contribute_data': row[4],
            'contribution_days': int(row[5]),
            'number_add_lines': int(row[6]),
            'number_del_lines': int(row[7]),
            'number_commits': int(row[8]),
            'repository': None
        }
        db.contributions.insert(data)
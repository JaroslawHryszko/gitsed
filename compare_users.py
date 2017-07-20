# loading libraries
from pymongo import MongoClient
import json, csv, pymongo, time, urllib, sys

# opening config file
with open('config.json') as json_data_file:
    config = json.load(json_data_file)

# opening connection with database
client = MongoClient(config['database']['server'])
db = client.github

#path to csv users file
csv_file = '<path>'

inexisting_users = 0

with open(csv_file, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        user = db.users.find({ 'login': row[2] }, no_cursor_timeout=True)
        if user.count() == 0:
            print inexisting_users
            inexisting_users = inexisting_users + 1

print 'Total inexisting users: ', inexisting_users

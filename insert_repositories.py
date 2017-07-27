# loading libraries
from pymongo import MongoClient
import json, csv, pymongo, time, urllib, sys

# opening config file
with open('config.json') as json_data_file:
    config = json.load(json_data_file)

# opening connection with database
client = MongoClient(config['database']['server'])
db = client.github

contributions = db.contributions.find({}, no_cursor_timeout=True)
for contribution in contributions:
    repository = db.repositories.find({ 'repository_id': contribution['repository_id']}, no_cursor_timeout=True)
    if repository.count() != 0:
        for repo in repository:
            del repo['_id']
            db.contributions.update({ '_id': contribution['_id'], 'repository_id': contribution['repository_id']}, { '$set': {'repository': repo}})
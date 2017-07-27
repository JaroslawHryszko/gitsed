# APPROACHES
# 1 - check inexisting users in sigsed dataset and ranking dataset
# 2 - insert inexisting users
# 3 - insert gitsed id
# 4 - check real inexisting users (once not all users in sigsed are being used)

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
#csv_file = '/Users/avenuecode/Downloads/DataSet/user.csv'

# INSERTING INEXISTING USERS TO DATASET
# inexisting_users = 0
# with open(csv_file, 'rb') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
#     for row in spamreader:
#         user = db.users.find({ 'login': row[2] }, no_cursor_timeout=True)
#         if user.count() == 0:
#             data = {}
#             data['gitsed'] = True
#             data['login'] = row[2]
#             json_data = json.dumps(data)
#             print inexisting_users, row[2]
#             inexisting_users = inexisting_users + 1
#             db.users.insert_one(data)
# print 'Total inexisting users: ', inexisting_users


#INSERTING GITSED USER ID
# csv_file = '/Users/avenuecode/Downloads/DataSet/user.csv'
# with open(csv_file, 'rb') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
#     for row in spamreader:
#         user = db.users.find({ 'login': row[2]}, no_cursor_timeout=True)
#         if user.count() != 0:
#             print row[0], row[2]
#             db.users.update_one({'login': row[2]}, {"$set": { "gitsed_id": row[0] }}, upsert=True)



# COMPARING REAL USERS
csv_file = '/Users/avenuecode/Downloads/DataSet/J_developers_social_network.csv'
with open(csv_file, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        print row
        user = db.users.find({ 'gitsed_id': int(row[1])}, no_cursor_timeout=True)
        if user.count() != 0:
            print 'developer 1', row[1]
            db.users.update_one({ 'gitsed_id': int(row[1])}, {"$set": { "gitsed_developer": True }}, upsert=True)
        user = db.users.find({ 'gitsed_id': int(row[2])}, no_cursor_timeout=True)
        if user.count() != 0:
            print 'developer 2', row[2]
            db.users.update_one({ 'gitsed_id': int(row[2])}, {"$set": { "gitsed_developer": True }}, upsert=True)



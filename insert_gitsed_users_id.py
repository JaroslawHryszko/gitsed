# loading libraries
from pymongo import MongoClient
import json, csv, pymongo, time, urllib, sys

# opening config file
with open('config.json') as json_data_file:
    config = json.load(json_data_file)

# opening connection with database
client = MongoClient(config['database']['server'])
db = client.github

csv_file = '/Users/avenuecode/Downloads/social_network_metrics.csv'
with open(csv_file, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        data = {
            "NO": float(row[3]),
            "AA": float(row[4]),
            "PA": float(row[5]),
            "SR": float(row[6]),
            "T_SR": float(row[7]),
            "RA_SR": float(row[8]),
            "JCSR": float(row[9]),
            "T_JCSR": float(row[10]),
            "RA_JCSR": float(row[11]),
            "JCOSR": float(row[12]),
            "T_JCOSR": float(row[13]),
            "RA_JCOSR": float(row[14]),
            "JWCOSR": float(row[15]),
            "T_JWCOSR": float(row[16]),
            "RA_JWCOSR": float(row[17]),
            "PC": float(row[18]),
            "T_PC": float(row[19]),
            "RA_PC": float(row[20]),
            "GPC": float(row[21]),
            "T_GPC": float(row[22]),
            "RA_GPC": float(row[23])
        }
        devs = []
        user_1 = db.users.find({ 'gitsed_id': int(row[1])}, no_cursor_timeout=True)
        user_2 = db.users.find({ 'gitsed_id': int(row[2])}, no_cursor_timeout=True)
        for user in user_1:
            devs.append({'developers._id': user['_id']})
        for user in user_2:
            devs.append({'developers._id': user['_id']})
        print devs
        if len(devs) == 2:
            contribution = db.contributions.find({ '$and': devs}, no_cursor_timeout=True)
            for cont in contribution:
                print cont['_id']
                db.contributions.update({ '_id': cont['_id']}, { '$set': {'metrics': data}}, upsert=False, multi=True)
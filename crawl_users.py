# loading libraries
from pymongo import MongoClient
import json, csv, pymongo, time, urllib, sys

# opening config file
with open('config.json') as json_data_file:
    config = json.load(json_data_file)

# opening connection with database
client = MongoClient(config['database']['server'])
db = client.github

# 1 - For each user, get the followers url
# 2 - Update the user with an array of followers
# 3 - If followers doesn't exist, collect them data
# 4 - Get the following url
# 5 - Update the user with an array of followings
# 6 - If following users doesn't exist, collect them data

followers_users = []
following_users = []

def print_limit_rate(response):
	response_headers = response.info()
	print response_headers.dict['x-ratelimit-remaining']
	if( int(response_headers.dict['x-ratelimit-remaining']) < 100 ):
		time.sleep(60)

def get_followers(user, page):
	try:
		url = "https://api.github.com/users/" + user['login'] + "/followers?page=" + str(page) + "&access_token=eb02fe76d01146e64371366777c6e3b88847a468"
		response = urllib.urlopen(url)
		print 'colleting followers: ' + user['login'] + " page: " + str(page)
		data = json.loads(response.read())

		if 'message' in data or len(data) == 0:
			print 'user not found'
			db.users.update_one({'login': user['login']}, {"$set": { "message": "Not Found"}}, upsert=True)
		else:
			if 'followers_users' not in user:
				user['followers_users'] = []
			for follower in data:
				user['followers_users'].append(follower['login'])
			db.users.update_one({'login': user['login']}, {"$unset": { "followers_users": "" } }, upsert=True)
			db.users.update_one({'login': user['login']}, {"$set": { "followers_users": user['followers_users']}}, upsert=True)

		print_limit_rate(response)
	except IOError:
		print 'Api GitHub is down'
		time.sleep(60)
		get_followers(user, page)

def get_following(user, page):
	url = "https://api.github.com/users/" + user['login'] + "/following?page=" + str(page) + "&access_token=eb02fe76d01146e64371366777c6e3b88847a468"
	try:
		response = urllib.urlopen(url)
		print 'colleting following: ' + user['login'] + " page: " + str(page)
		data = json.loads(response.read())
		
		if 'message' in data or len(data) == 0:
			print 'user not found'
			db.users.update_one({'login': user['login']}, {"$set": { "message": "Not Found"}}, upsert=True)
		else:
			if 'following_users' not in user:
				user['following_users'] = []
			for follower in data:
				user['following_users'].append(follower['login'])
			db.users.update_one({'login': user['login']}, {"$unset": { "following_users": "" } }, upsert=True)
			db.users.update_one({'login': user['login']}, {"$set": { "following_users": user['following_users']}}, upsert=True)

		print_limit_rate(response)
	except IOError:
		print 'Api GitHub is down'
		time.sleep(60)
		get_following(user, page)

def collect_user(user):
	url = "https://api.github.com/users/" + user + "?access_token=eb02fe76d01146e64371366777c6e3b88847a468"
	try:
		response = urllib.urlopen(url)
		print 'colleting user: ' + user
		data = json.loads(response.read())

		try:
			db.users.insert_one(data)
		except pymongo.errors.DuplicateKeyError:
			print 'user already exists'

		print_limit_rate(response)
	except IOError:
		print 'Api GitHub is down'
		time.sleep(60)
		collect_user(user)

def update_user(user):
    url = "https://api.github.com/users/" + user + "?access_token=eb02fe76d01146e64371366777c6e3b88847a468"
    try:
        response = urllib.urlopen(url)
        print 'colleting user: ' + user
        data = json.loads(response.read())

        try:
            if 'login' in data:
                del data['login']
            db.users.update_one({ 'login': user}, {"$set": data}, upsert=True)
        except pymongo.errors.DuplicateKeyError as e:
            print 'user already exists', e

        print_limit_rate(response)
    except IOError:
        print 'Api GitHub is down'
        time.sleep(60)
        update_user(user)

users = db.users.find({ 'gitsed_developer': True, 'following': { '$exists': False }, 'message': {'$exists': False} }, no_cursor_timeout=True)
for user in users:
    update_user(user['login'])
	# if user['followers'] > 0:
	# 	if 'followers_users' not in user:
	# 		amountPagesFollowers = int( user['followers'] / 30 ) + 2 
	# 		for page in range( 1, amountPagesFollowers ):
	# 			get_followers(user, page)
	
	# if user['following'] > 0:
	# 	if 'following_users' not in user:
	# 		amountPagesFollowing = int( user['following'] / 30 ) + 2 
	# 		for page in range( 1, amountPagesFollowing ):
	# 			get_following(user, page)


	# if 'followers_users' in user:
	# 	for followers_user in user['followers_users']:
	# 		if db.users.find({ 'login': followers_user }).count() > 0:
	# 			print 'user already exists'
	# 		else:
	# 			collect_user(followers_user)


	# if 'following_users' in user:
	# 	for following_user in user['following_users']:
	# 		if db.users.find({ 'login': following_user }).count() > 0:
	# 			print 'user already exists'
	# 		else:
	# 			collect_user(following_user)


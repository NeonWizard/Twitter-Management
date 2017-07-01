# import urllib.request

# req = urllib.request.Request("https://api.heroku.com/apps/immense-refuge-73091/config-vars")
# req.add_header("Accept", "application/vnd.heroku+json; version=3")
# req.add_header("Authorization", "Bearer {}".format("1d2e52e6-a0b2-41c8-b9c7-0d08acf6dd44"))

# with urllib.request.urlopen(req) as cvarFile:
# 	for line in cvarFile:
# 		print(line)

import os, sys
import time
from twython import Twython, TwythonError, TwythonRateLimitError
from boto.s3.connection import S3Connection

twitterAPI = Twython(os.environ["TWITTER_API_KEY"], os.environ["TWITTER_API_SECRET"], os.environ["TWITTER_TOKEN"], os.environ["TWITTER_TOKEN_SECRET"])
s3API = S3Connection(os.environ["S3_KEY"], os.environ["S3_SECRET_KEY"])

key = s3API.get_bucket("wespooky-twittermanagement").get_key("followers.txt")

# ======================
#   -=- CODE TIME -=-
# ======================

# == Load Sets ==
lastrunFollowers = set([int(follower) for follower in key.get_contents_as_string().decode().split("|")])
currentFollowers = set(twitterAPI.get_followers_ids()["ids"])

# == Follow Back ==
# DESC: Follow everyone in current follower list who isn't in lastrun follower list
toFollow = currentFollowers.difference(lastrunFollowers)

for ID in toFollow:
	try:
		user = twitterAPI.show_user(user_id=ID)

		twitterAPI.create_friendship(user_id=ID)
		sys.stdout.write("Followed {} (@{}) back.".format(user["name"], user["screen_name"]))

	except: # Rate limit or 404 (should probably do special stuff here later)
		pass

# == Unfollow Unfollowers ==
# DESC: Unfollow everyone in lastrun follower list who isn't in current follower list.
toUnfollow = lastrunFollowers - currentFollowers

for ID in toUnfollow:
	try:
		user = twitterAPI.show_user(user_id=ID)

		twitterAPI.destroy_friendship(user_id=ID)
		sys.stdout.write("Unfollowed {} (@{}).".format(user["name"], user["screen_name"]))

	except:
		pass


# == Save Set ==
key.set_contents_from_string(
	"|".join([str(follower) for follower in currentFollowers])
)

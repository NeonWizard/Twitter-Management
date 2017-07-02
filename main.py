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
		sys.stdout.write("Followed {} (@{}) back.\n".format(user["name"], user["screen_name"]))

	except: # Rate limit or 404 (should probably do special stuff here later)
		pass

# == Unfollow Unfollowers ==
# DESC: Unfollow everyone in lastrun follower list who isn't in current follower list.
toUnfollow = lastrunFollowers - currentFollowers

for ID in toUnfollow:
	try:
		user = twitterAPI.show_user(user_id=ID)

		twitterAPI.destroy_friendship(user_id=ID)
		sys.stdout.write("Unfollowed {} (@{}).\n".format(user["name"], user["screen_name"]))

	except:
		pass

sys.stdout.flush()

# == Save Set ==
key.set_contents_from_string(
	"|".join([str(follower) for follower in currentFollowers])
)

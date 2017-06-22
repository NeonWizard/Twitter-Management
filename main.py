# import urllib.request

# req = urllib.request.Request("https://api.heroku.com/apps/immense-refuge-73091/config-vars")
# req.add_header("Accept", "application/vnd.heroku+json; version=3")
# req.add_header("Authorization", "Bearer {}".format("1d2e52e6-a0b2-41c8-b9c7-0d08acf6dd44"))

# with urllib.request.urlopen(req) as cvarFile:
# 	for line in cvarFile:
# 		print(line)

import os
import time
from twython import Twython, TwythonError, TwythonRateLimitError
from boto.s3.connection import S3Connection

twitter_api = Twython(os.environ["TWITTER_API_KEY"], os.environ["TWITTER_API_SECRET"], os.environ["TWITTER_TOKEN"], os.environ["TWITTER_TOKEN_SECRET"])
s3_api = S3Connection(os.environ["S3_KEY"], os.environ["S3_SECRET"])

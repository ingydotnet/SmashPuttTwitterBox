import threading
import tweepy
from settings import *
from custom_stream_listener import CustomStreamListener
class Watcher(threading.Thread):
	#----------------------------------------------------------------------
	def __init__(self, queue, logger):
		threading.Thread.__init__(self)
		self.queue = queue
		self.logger = logger
		self.logger.debug("Twitter watcher created")
		self.auth = None
		self.api = None

	#----------------------------------------------------------------------
	def authenticate(self):
		self.logger.info("Authenticating to twitter")
		try:
			self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
			self.auth.set_access_token(access_key, access_secret)
			self.api = tweepy.API(self.auth)
		except Exception as e:
			self.logger.error("Could not authenticate: " + str(e))

	#----------------------------------------------------------------------
	def run(self):
		if not self.auth or not self.api:
			self.authenticate()
			
		try:
			listener = CustomStreamListener(self.queue, self.logger)
			stream = tweepy.streaming.Stream(self.auth, listener)
			self.logger.info("Starting twitter stream")
			stream.filter(track=track)
			self.logger.error("Twitter stream closed")
		except Exception as e:
			self.logger.error("Disconnected from twitter: " + str(e))

	#----------------------------------------------------------------------
	def getUserData(self):
		if not self.auth or not self.api:
			self.authenticate()

		try:
			user = self.api.get_user(screen_name)
			user_data = {"@" + screen_name + ":": "Followers: " + str(user.followers_count)}
			return user_data
		except Exception as e:
			self.logger.error("Could not get data for " + screen_name + ": " + str(e))


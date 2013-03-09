import threading
import tweepy
import time

from custom_stream_listener import CustomStreamListener
import settings

class Watcher(threading.Thread):
	#----------------------------------------------------------------------
	def __init__(self, queue, logger):
		threading.Thread.__init__(self)
		self.queue = queue
		self.logger = logger
		self.logger.debug("Twitter watcher created")
		self.auth = None

	#----------------------------------------------------------------------
	def authenticate(self):
		self.logger.info("Authenticating to twitter")
		try:
			self.auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
			self.auth.set_access_token(settings.ACCESS_KEY, settings.ACCESS_SECRET)
		except Exception as e:
			self.logger.error("Could not authenticate: " + str(e))

	#----------------------------------------------------------------------
	def get_api(self):
		if not self.auth:
			self.authenticate()
		return tweepy.API(self.auth)

	#----------------------------------------------------------------------
	def run(self):
		if not self.auth:
			self.authenticate()
			
		try:
			listener = CustomStreamListener(self.queue, self.logger)
			stream = tweepy.streaming.Stream(self.auth, listener, secure=True, headers={'User-Agent':'SmashPuttTwitterBox'})
			self.logger.info("Starting twitter stream")
			stream.filter(track=settings.TRACK)
			self.logger.error("Twitter stream closed")
			if listener.rate_limited:
				self.logger.debug("Sleeping for a minute to clear rate limit")
				time.sleep(60)
		except Exception as e:
			self.logger.error("Disconnected from twitter: " + str(e))

	#----------------------------------------------------------------------
	def getUserData(self):
		api = get_api()

		try:
			user = api.get_user(settings.SCREEN_NAME)
			user_data = {"@" + settings.SCREEN_NAME + ":": "Followers: " + str(user.followers_count)}
			return user_data
		except Exception as e:
			self.logger.error("Could not get data for " + settings.SCREEN_NAME + ": " + str(e))


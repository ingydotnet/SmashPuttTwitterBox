import tweepy
import time
from settings import *
class CustomStreamListener(tweepy.StreamListener):
	#----------------------------------------------------------------------
	def __init__(self, queue, logger):
		tweepy.StreamListener.__init__(self)
		self.queue = queue
		self.logger = logger
		self.logger.debug("Twitter listener created")

	#----------------------------------------------------------------------
	def on_status(self, status):
		self.queue.put((PRIORITY_HIGH, "@" + status.user.screen_name + ":", status.text, True))

	#----------------------------------------------------------------------
	def on_error(self, status_code):
		if status_code == 420:
			self.logger.error("Hit the rate limit for twitter... sleeping for a minute")
			time.sleep(60)
		else:
			self.logger.error("Encountered error with status code: " + str(status_code))
		return True # Don't kill the stream

	#----------------------------------------------------------------------
	def on_timeout(self):
		self.logger.error("Twitter Timeout...")
		return True # Don't kill the stream


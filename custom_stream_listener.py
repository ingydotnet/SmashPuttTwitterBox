import tweepy
import HTMLParser
import settings

class CustomStreamListener(tweepy.StreamListener):
	#----------------------------------------------------------------------
	def __init__(self, queue, logger):
		tweepy.StreamListener.__init__(self)
		self.queue = queue
		self.logger = logger
		self.logger.debug("Twitter listener created")
		self.parser = HTMLParser.HTMLParser()
		self.rate_limited = False
		self.status_count = 0

	#----------------------------------------------------------------------
	def on_status(self, status):
		self.status_count = self.status_count + 1
		self.logger.debug("Status(" + str(self.status_count) + "): " + status.text)
		self.queue.put((settings.PRIORITY_HIGH, "@" + status.user.screen_name + ":", self.parser.unescape(status.text), True))

	#----------------------------------------------------------------------
	def on_error(self, status_code):
		if status_code == 420:
			self.logger.error("Hit the rate limit for twitter!!!")
			self.rate_limited = True
			return False
		else:
			self.logger.error("Encountered error with status code: " + str(status_code))
		return True # Don't kill the stream

	#----------------------------------------------------------------------
	def on_timeout(self):
		self.logger.error("Twitter Timeout...")
		return True # Don't kill the stream


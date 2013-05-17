#!/usr/bin/python

try:
	import RPi.GPIO as GPIO
	PI = True
except ImportError:
	PI = False

import logging
import Queue
import time
import os
from watcher import Watcher
from printer import Printer
import sys
import traceback
import settings

def main():
	# Setup Logging
	logger = logging.getLogger('twitterbox')
	hdlr = logging.FileHandler(settings.LOG)
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr) 

	hdlr = logging.StreamHandler(sys.stdout)
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr) 
	if settings.DEBUG:
		logger.setLevel(logging.DEBUG)
		logger.info("DEBUG level logging")
	else:
		logger.setLevel(logging.INFO)
		logger.info("INFO level logging")
	logger.info("Starting up...")

	if PI:
		# Not interested
		GPIO.setwarnings(False)

		# Setup the LCD display
		GPIO.setmode(GPIO.BCM)	     # Use BCM GPIO numbers

		# Setup the alert light
		GPIO.setup(settings.LIGHT_PIN, GPIO.OUT) 
		GPIO.output(settings.LIGHT_PIN, GPIO.LOW)


	# The queue is where messages go to be displayed
	queue = Queue.PriorityQueue()
	
	watcher = None
	printer = None
	loops = 0
	while True:
		try:
			loops = loops + 1
			logger.debug("Main Loop " + str(loops))

			# Make sure our twitter thread is alive and happy
			if not watcher or not watcher.is_alive():
				logger.info("Starting watcher thread")
				watcher = Watcher(queue, logger)
				watcher.setDaemon(True)
				watcher.start()

			# Make sure our printing thread is alive and happy
			if not printer or not printer.is_alive():
				logger.info("Starting printer thread")
				printer = Printer(queue, logger, PI)
				printer.setDaemon(True)
				printer.start()

			# Throw some info in the queue if it's getting low
			if queue.qsize() == 0:
				messages = open(settings.MSG_FILE, 'r')
				for msg in messages:
					queue.put((settings.PRIORITY_LOW, msg, "", False))
				messages.close()
				
				# Switching to using the message file instead of this generated msg
				#for w in settings.TRACK:
				#	queue.put((settings.PRIORITY_LOW, "Watching for:", w, False))
				
				# We are not tracking the number of followers for this event
				# This frees up an extra twitter connection to avoid rate limiting --JLS
				# user_data = watcher.getUserData()
				# if user_data != None:
				# 	for k,v in user_data.iteritems():
				# 		queue.put((PRIORITY_LOW, k, v, False))
		except Exception as e:
			logger.error("Exception in main thread: " + str(e))
			traceback.print_tb(sys.exc_info()[2])

		time.sleep(15)

	logger.warn("Exiting main thread")


if __name__ == '__main__':
	main()

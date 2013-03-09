from settings import *

import os
import sys
import time
import Queue
import logging
import traceback
from watcher import Watcher

def main():
	# Setup Logging
	logger = logging.getLogger('twitterbox')
	hdlr = logging.StreamHandler(sys.stdout)
	formatter = logging.Formatter('%(asctime)s %(module)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr) 
	logger.setLevel(logging.DEBUG)
			
	queue = Queue.PriorityQueue()
	
	watcher = None
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

			# Dump the queue
			for m in range(queue.qsize()):
				msg = queue.get()
				priority = msg[0]
				line1 = msg[1]
				line2 = msg[2]
				alert = msg[3]
				logger.info(line1 + " " + line2)
				queue.task_done()
				
		except Exception as e:
			logger.error("Exception in main thread: " + str(e))
			traceback.print_tb(sys.exc_info()[2])

		time.sleep(15)

	logger.warn("Exiting main thread")


if __name__ == '__main__':
	main()

import threading
import time
import Queue
from video import Video
from settings import *
try:
	import RPi.GPIO as GPIO
	PI = True
except ImportError:
	PI = False
class Printer(threading.Thread):
	#----------------------------------------------------------------------
	def __init__(self, queue, logger, pi):
		threading.Thread.__init__(self)
		self.queue = queue
		self.pi = pi
		self.logger = logger
		self.logger.debug("Twitter printer created")
		self.videoQueue = Queue.PriorityQueue(1)

	#----------------------------------------------------------------------
	def run(self):
		video = None
		while True:
			# Make sure our printing thread is alive and happy
			if not video or not video.is_alive():
				self.logger.info("Starting video thread")
				video = Video(self.logger, self.videoQueue, self.queue)
				video.setDaemon(True)
				video.start()

			try:
				# Pull the message from the queue
				msg = self.queue.get()
				self.videoQueue.put(msg)
				priority = msg[0]
				line1 = msg[1]
				line2 = msg[2]
				alert = msg[3]

				if priority == PRIORITY_HIGH:
					self.logger.info(line1 + " " + line2)
				
				# If we should turn the light on, do it
				if (alert):
					if self.pi:
						self.logger.debug("Light on...")
						GPIO.output(LIGHT_PIN, GPIO.HIGH)

					time.sleep(LIGHT_DELAY)

					if self.pi:
						self.logger.debug("Light off")
						GPIO.output(LIGHT_PIN, GPIO.LOW)
				else:
					time.sleep(5)

				# All done!
				self.queue.task_done()
				self.logger.debug("Finished queue item. Queue size: " + self.queue.qsize())
			except Exception as e:
				self.logger.error("Exception in printer: " + str(e))


import threading
import time
from settings import *
class Printer(threading.Thread):
	#----------------------------------------------------------------------
	def __init__(self, queue, logger, pi):
		threading.Thread.__init__(self)
		self.queue = queue
		self.pi = pi
		self.logger = logger
		self.logger.debug("Twitter printer created")

	#----------------------------------------------------------------------
	def run(self):
		while True:
			try:
				# Pull the message from the queue
				msg = self.queue.get()
				priority = msg[0]
				line1 = msg[1]
				line2 = msg[2]
				alert = msg[3]
				if priority == PRIORITY_HIGH:
					self.logger.info(line1 + " " + line2)
				
				if self.pi:
					# Clear the LCD and write the message
					lcd_init()
					lcd_byte(LCD_LINE_1, LCD_CMD)
					lcd_string(line1[:16])
					lcd_byte(LCD_LINE_2, LCD_CMD)
					lcd_string(line2[:16])

				# If we should turn the light on, do it
				if (alert):
					if self.pi:
						self.logger.debug("Light on...")
						GPIO.output(LIGHT_PIN, GPIO.HIGH)
						time.sleep(LIGHT_DELAY)
						self.logger.debug("Light off")
						GPIO.output(LIGHT_PIN, GPIO.LOW)
				else:
					time.sleep(5)

				# All done!
				self.queue.task_done()
			except Exception as e:
				self.logger.error("Exception in printer: " + str(e))


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

					if self.pi:
						self.logger.debug("Light off")
						GPIO.output(LIGHT_PIN, GPIO.LOW)
				else:
					time.sleep(5)

				# All done!
				self.queue.task_done()
			except Exception as e:
				self.logger.error("Exception in printer: " + str(e))

	def lcd_init():
		# Initialise display
		lcd_byte(0x33,LCD_CMD)
		lcd_byte(0x32,LCD_CMD)
		lcd_byte(0x28,LCD_CMD)
		lcd_byte(0x0C,LCD_CMD)	
		lcd_byte(0x06,LCD_CMD)
		lcd_byte(0x01,LCD_CMD)	

	def lcd_string(message):
		# Send string to display
		message = message.ljust(LCD_WIDTH," ")	
		for i in range(LCD_WIDTH):
			lcd_byte(ord(message[i]),LCD_CHR)

	def lcd_byte(bits, mode):
		# Send byte to data pins
		# bits = data
		# mode = True for character
		#			False for command
		GPIO.output(LCD_RS, mode) # RS

		# High bits
		GPIO.output(LCD_D4, False)
		GPIO.output(LCD_D5, False)
		GPIO.output(LCD_D6, False)
		GPIO.output(LCD_D7, False)
		if bits&0x10==0x10:
			GPIO.output(LCD_D4, True)
		if bits&0x20==0x20:
			GPIO.output(LCD_D5, True)
		if bits&0x40==0x40:
			GPIO.output(LCD_D6, True)
		if bits&0x80==0x80:
			GPIO.output(LCD_D7, True)

		# Toggle 'Enable' pin
		time.sleep(E_DELAY)		 
		GPIO.output(LCD_E, True)	
		time.sleep(E_PULSE)
		GPIO.output(LCD_E, False)	 
		time.sleep(E_DELAY)			 

		# Low bits
		GPIO.output(LCD_D4, False)
		GPIO.output(LCD_D5, False)
		GPIO.output(LCD_D6, False)
		GPIO.output(LCD_D7, False)
		if bits&0x01==0x01:
			GPIO.output(LCD_D4, True)
		if bits&0x02==0x02:
			GPIO.output(LCD_D5, True)
		if bits&0x04==0x04:
			GPIO.output(LCD_D6, True)
		if bits&0x08==0x08:
			GPIO.output(LCD_D7, True)

		# Toggle 'Enable' pin
		time.sleep(E_DELAY)		 
		GPIO.output(LCD_E, True)	
		time.sleep(E_PULSE)
		GPIO.output(LCD_E, False)	 
		time.sleep(E_DELAY)		

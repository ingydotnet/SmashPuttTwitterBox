#!/usr/bin/python

from settings import *
try:
	import RPi.GPIO as GPIO
	PI = True
except:
	PI = False

import logging
import Queue
import time
import os
from watcher import Watcher
from printer import Printer
import sys
import traceback


def main():
	# Setup Logging
	logger = logging.getLogger('twitterbox')
	#hdlr = logging.FileHandler(LOG)
	hdlr = logging.StreamHandler(sys.stdout)
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr) 
	if DEBUG:
		logger.setLevel(logging.DEBUG)
	else:
		logger.setLevel(logging.INFO)
	logger.info("Starting up...")

	if PI:
		# Not interested
		GPIO.setwarnings(False)

		# Setup the LCD display
		GPIO.setmode(GPIO.BCM)	     # Use BCM GPIO numbers
		GPIO.setup(LCD_E, GPIO.OUT)  # E
		GPIO.setup(LCD_RS, GPIO.OUT) # RS
		GPIO.setup(LCD_D4, GPIO.OUT) # DB4
		GPIO.setup(LCD_D5, GPIO.OUT) # DB5
		GPIO.setup(LCD_D6, GPIO.OUT) # DB6
		GPIO.setup(LCD_D7, GPIO.OUT) # DB7

		# Setup the alert light
		GPIO.setup(LIGHT_PIN, GPIO.OUT) 
		GPIO.output(LIGHT_PIN, GPIO.LOW)


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
				for w in track:
					queue.put((PRIORITY_LOW, "Watching for:", w, False))
				user_data = watcher.getUserData()
				for k,v in user_data.iteritems():
					queue.put((PRIORITY_LOW, k, v, False))
		except Exception as e:
			logger.error("Exception in main thread: " + str(e))
			traceback.print_tb(sys.exc_info()[2])

		time.sleep(15)

	logger.warn("Exiting main thread")

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

if __name__ == '__main__':
	main()

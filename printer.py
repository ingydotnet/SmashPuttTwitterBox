import threading
import time
import pygame
from pygame import camera
from settings import *
from textwrap import *
class Printer(threading.Thread):
	#----------------------------------------------------------------------
	def __init__(self, queue, logger, pi):
		threading.Thread.__init__(self)
		self.queue = queue
		self.pi = pi
		self.logger = logger
		self.logger.debug("Twitter printer created")

		# Setup screen
		pygame.init()
		self.width = 1024
		self.height = 768
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.font = pygame.font.SysFont("Droid Sans Mono", 32, bold=1)


		camera.init()
		self.c = camera.Camera('/dev/video0', (640,480))
		self.c.start()
		self.surface = self.c.get_image()
		self.bigSurface = None

		self.c.get_image(self.surface)
		self.bigSurface = pygame.transform.scale(self.surface, (self.width, self.height))
		self.screen.blit(self.bigSurface, (0,0))
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
					line_length = 45
					wrapped_text = wrap(line1 + ' ' + line2, line_length)
					for index, line in enumerate(wrapped_text):
						textSurface = self.font.render(line, 1, pygame.Color(255, 0, 0))
						self.screen.blit(textSurface, (1,(index * self.font.get_height())+1))
					pygame.display.update()

					if self.pi:
						self.logger.debug("Light on...")
						GPIO.output(LIGHT_PIN, GPIO.HIGH)

					time.sleep(LIGHT_DELAY)

					if self.pi:
						self.logger.debug("Light off")
						GPIO.output(LIGHT_PIN, GPIO.LOW)
				# else:
				# 	time.sleep(5)

				if self.c.query_image():
					self.c.get_image(self.surface)
					self.bigSurface = pygame.transform.scale(self.surface, (self.width, self.height))
				if self.bigSurface != None:
					self.screen.blit(self.bigSurface, (0,0))

				# All done!
				self.queue.task_done()
			except Exception as e:
				self.logger.error("Exception in printer: " + str(e))


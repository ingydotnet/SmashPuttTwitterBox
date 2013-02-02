import threading
import pygame
import Queue
import sys
from pygame import camera
from textwrap import *
from die import Die
class Video(threading.Thread):
	def __init__(self, logger, queue):
		threading.Thread.__init__(self)
		self.logger = logger
		self.queue = queue
		self.logger.debug("Video created")

		self.text = "Welcome to Smash Putt"

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
		self.pause = False

		self.c.get_image(self.surface)
		self.bigSurface = pygame.transform.scale(self.surface, (self.width, self.height))
		self.screen.blit(self.bigSurface, (0,0))

	def run(self):
		while True:
			try:
				try:
					msg = self.queue.get_nowait()
					priority = msg[0]
					line1 = msg[1]
					line2 = msg[2]
					alert = msg[3]
					self.pause = alert
					self.text = line1 + ' ' + line2
					self.queue.task_done()
					self.c.get_image(self.surface)
					self.bigSurface = pygame.transform.scale(self.surface, (self.width, self.height))
				except Queue.Empty:
					self.logger.debug("Video queue empty")

				if not self.pause:
					if self.c.query_image():
						self.c.get_image(self.surface)
						self.bigSurface = pygame.transform.scale(self.surface, (self.width, self.height))
				if self.bigSurface != None:
					self.screen.blit(self.bigSurface, (0,0))

				if self.text != None:
					line_length = 45
					wrapped_text = wrap(self.text, line_length)
					for index, line in enumerate(wrapped_text):
						textSurface = self.font.render(line, True, pygame.Color(255, 0, 0))
						shadow = self.font.render(line, True, pygame.Color(0, 0, 0))
						pos = (1,index * self.font.get_linesize())
						shadowOffset = 3
						self.screen.blit(shadow, (pos[0]+shadowOffset, pos[1]+shadowOffset))
						self.screen.blit(textSurface, pos)

				pygame.display.update()

			except Exception as e:
				self.logger.error("Exception in video: " + str(e))


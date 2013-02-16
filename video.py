import threading
import pygame
import Queue
import os
from pygame import camera
from textwrap import *
class Video(threading.Thread):
	def __init__(self, logger, queue, parent_queue):
		threading.Thread.__init__(self)
		self.logger = logger
		self.queue = queue
		self.parent_queue = parent_queue
		self.logger.debug("Video created")

		self.text = "Welcome to Smash Putt"

		# Setup screen
		pygame.init()
		pygame.mouse.set_visible(False)
		self.width = 1024
		self.height = 768
		self.screen = pygame.display.set_mode((self.width, self.height))
		font_size = 60
		font_width = font_size * 0.68956
		font_width = font_size * 0.7
		self.font = pygame.font.SysFont("Droid Sans Mono", font_size, bold=1)
		self.line_length = self.width/font_width


		camera.init()
		camera_size = (640,480)
		self.c = camera.Camera('/dev/video0', camera_size)
		self.c.start()
		self.surface = pygame.Surface(camera_size)
		self.bigSurface = None
		self.pause = False

		self.foregroundColor = pygame.Color(255, 0, 0)
		self.black = pygame.Color(0, 0, 0)
		self.shadowShade = 0

	def run(self):
		new_text = False
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
					new_text = True
					self.queue.task_done()
				except Queue.Empty:
					False
					#self.logger.debug("Video queue empty")


				if new_text or not self.pause:
					new_text = False
					if self.c.query_image():
						self.c.get_image(self.surface)
						self.logger.debug( "Captured image")
						self.bigSurface = pygame.transform.scale(self.surface, (self.width, self.height))
					if self.bigSurface != None:
						self.screen.blit(self.bigSurface, (0,0))

				if self.text != None:
					wrapped_text = wrap(self.text, self.line_length)
					for index, line in enumerate(wrapped_text):
						textSurface = self.font.render(line, True, self.foregroundColor)
						shadowColor = self.black
						if self.pause:
							self.shadowShade = (self.shadowShade + 3) % 255
							shadowColor = pygame.Color(self.shadowShade, self.shadowShade, self.shadowShade)
						shadow = self.font.render(line, True, shadowColor)
						pos = (1,index * self.font.get_linesize())
						shadowOffset = 3
						self.screen.blit(shadow, (pos[0]+shadowOffset, pos[1]+shadowOffset))
						self.screen.blit(textSurface, pos)

				pygame.display.update()
				
				for event in pygame.event.get():
					if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key ==pygame.K_q:
						self.logger.info("EXIT")
						pygame.quit()
						os._exit(0)
					if event.type == pygame.KEYDOWN and event.key ==pygame.K_t:
						msg = [1, "This is a test line 1", "message line 2", True]
						self.parent_queue.put(msg)
			except Exception as e:
				self.logger.error("Exception in video: " + str(e))


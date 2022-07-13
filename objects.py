import pygame
from helperFunctions import *

class Object():
	""" Representation of any object, other than the player """

	def __init__(self, x, y, speed, renderVal, frames, col = 1):
		self.xPos = x			# location in the level
		self.yPos = y			# location in the level
		self.animFrames = {}
		self.speed = speed
		self.collisionType = col	# 0 = no collision, 1 = death, 2 = block
		self.renderVal = renderVal	# order in which objects are rendered
		for no, frame in enumerate(frames):
			self.animFrames[no] = pygame.image.load(frame)
		self.counter = RangeIterator(len(self.animFrames) - 1)


	def update(self):
		if pygame.time.get_ticks() % 5 == 0:
			self.counter.inc()
		self.currentFrame = self.animFrames[self.counter.get()]
		self.mask = pygame.mask.from_surface(self.currentFrame)
		self.xPos -= self.speed








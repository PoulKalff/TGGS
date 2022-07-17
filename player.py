import time
import pygame
import random
from helperFunctions import *


class Player():
	""" Representation of the player """

	def __init__(self, parent):
		self.parent = parent
		self.vector = 1				# last direction, left or right
		self.movement = PlayerMovement()
		self.stationary = 0
		self.goingUp = False
		self.kneeling = False
		self.death = 0
		self.changetime = 0
		self.standFrame = pygame.image.load('gfx/animRun/standing.png')
		self.kneelFrame = pygame.image.load('gfx/animRun/kneeling.png')
		self.kneelHeadFrame = pygame.image.load('gfx/animHead/kneeling.png')
		self.jumpFrames = {0: pygame.image.load('gfx/animRun/jumpUp.png'), 1 : pygame.image.load('gfx/animRun/jumpDown.png')}
		self.runFrames = {nr : pygame.image.load('gfx/animRun/' + str(nr + 1) + '.png') for nr in range(20)}
		self.headFrames = {nr : pygame.image.load('gfx/animHead/' + str(nr + 1) + '.png') for nr in range(8)}
		self.headDeath  = {0 : pygame.image.load('gfx/animHead/death1.png'), 1 : pygame.image.load('gfx/animHead/death2.png'), 2 : pygame.image.load('gfx/animHead/death1.png')}
		self.deathScreens = [pygame.image.load('gfx/deathScreen1.png'), pygame.image.load('gfx/deathScreen2.png')]
		self.deathSounds = [pygame.mixer.Sound('sfx/death3.mp3'), pygame.mixer.Sound('sfx/death1.mp3'), pygame.mixer.Sound('sfx/death2.mp3'), pygame.mixer.Sound('sfx/death3.mp3'),
							pygame.mixer.Sound('sfx/death2.mp3'), pygame.mixer.Sound('sfx/death1.mp3'), pygame.mixer.Sound('sfx/death2.mp3'), pygame.mixer.Sound('sfx/death3.mp3')]
		self.bodyFrameNo = RangeIterator(19)
		self.headFrameNo = RangeIterator(3)
		self.currentBody = self.runFrames[self.bodyFrameNo.get()]
		self.currentHead = self.headFrames[0]
		y, x  = pygame.display.get_surface().get_size()
		self.size = self.runFrames[1].get_rect().size
		self.yAcc = 30
		self.xPos = 300
		self.yPosLevel = x - self.runFrames[1].get_height() - 40
		self.yPos = self.yPosLevel
		self.xPosMin = 350
		self.xPosMax = 650


	def onGround(self):
		return self.yPos == self.yPosLevel


	def showDeath(self):
		""" paint 10 heads flying in different directions, from starting point """
		self.parent.backgroundMusic.stop()
		posMatrix = [
						[[0, 10], [2, -24], [-34, -39], [-59, -26], [8, 5], [10, 38], [12, 91], [16, 176], [20, 312], [25, 529], [30, 846]] ,
						[[0, -24], [10, -39], [20, -26], [30, 5], [45, 38], [60, 91], [85, 176], [110, 312], [150, 529], [200, 846], [250, 1000]] ,
						[[0, -39], [50, -26], [100, 5], [150, 38], [175, 91], [200, 176], [225, 312], [250, 529], [275, 846], [265, 1000], [270, 1000]] ,
						[[0, -26], [25, 5], [50, 38], [75, 91], [87, 176], [100, 312], [112, 529], [125, 846], [137, 1000], [132, 1000], [122, 1000]] ,
						[[0, 5], [25, 38], [50, 91], [75, 176], [87, 312], [100, 529], [112, 846], [125, 1000], [137, 1000], [132, 1000], [122, 1000]] ,
						[[0, 38], [32, 91], [65, 176], [97, 312], [113, 529], [130, 846], [145, 1000], [162, 1000], [178, 1000], [171, 1000], [158, 1000]] 
					]
		if self.death == 1:
			pygame.mixer.stop()
			for head in self.deathSounds:
				time.sleep(random.randint(0,4) / 100)
				head.set_volume(random.randint(2,6) / 100)
				head.play()
		time.sleep(0.05)	# slow down animation. Should be locked to ticks!
		if self.death < 12:
			for head in range(6):
				self.parent.renderList.append(renderObject(self.headDeath[random.randint(0,2)], (self.xPos + posMatrix[head][self.death - 1][0], self.yPos - 20 + posMatrix[head][self.death - 1][1]), 100, 'random death head right'))
				self.parent.renderList.append(renderObject(self.headDeath[random.randint(0,2)], (self.xPos - posMatrix[head][self.death - 1][0], self.yPos - 20 + posMatrix[head][self.death - 1][1]), 100, 'random death head left'))
		elif self.death < 20:	# pausing
			pass
		elif self.death < 45:
				self.parent.renderList.append(renderObject(self.deathScreens[0] , (0, 0), 100, 'first Death-screen'))
		elif self.death < 70:
				self.parent.renderList.append(renderObject(self.deathScreens[1] , (0, 0), 100, 'second Death-screen'))
		else:
		 	self.parent.initGame()
		self.death += 1
		return 1



	def update(self):
		self.calculateJump()
		self.changeBody()
		self.changeHead()
		self.bodyMask = pygame.mask.from_surface(self.currentBody)
		self.headMask = pygame.mask.from_surface(self.currentHead)
		if pygame.time.get_ticks() - self.changetime >= 1000:	# change head every second
			self.headFrameNo.inc()
			self.changetime = pygame.time.get_ticks()
		if self.movement.isMoving():
			self.stationary = 0
		else:
			self.stationary += 1
			self.stop()
		if self.death:
			self.showDeath()
		else:
			self.parent.renderList.append(renderObject(self.currentBody, (self.xPos, self.yPos), 100, 'player body'))
			self.parent.renderList.append(renderObject(self.currentHead, self.getHeadCoord(), 100, 'player head'))



	def changeBody(self):
		if self.onGround():
			if self.movement.left or self.movement.right:
				self.currentBody = self.runFrames[self.bodyFrameNo.get()]
			else:
				self.currentBody = self.kneelFrame if self.kneeling else self.standFrame
		elif self.goingUp:
			self.currentBody = self.jumpFrames[0] 		# going up
		else:
			self.currentBody = self.jumpFrames[1]		# going down
		if not self.vector:
			self.currentBody = pygame.transform.flip(self.currentBody, True, False)



	def changeHead(self):
		value = 0 if self.stationary < 50 else 4	# added to use headFrame 4 - 8, if player is idle
		self.currentHead = self.kneelHeadFrame if self.kneeling else self.headFrames[self.headFrameNo.get() + value]
		if not self.vector:
			self.currentHead = pygame.transform.flip(self.currentHead, True, False)


	def calculateJump(self):
		if self.goingUp and self.yPos > 200:
			self.yPos -= 15
			self.movement.goUp()
		else:
			self.goingUp = False
			if self.yPos < self.yPosLevel:		# if player is in the air 
				self.movement.goDown()
				self.yPos += 10			# gravity
				if self.yPos > self.yPosLevel:
					self.yPos = self.yPosLevel


	def move(self, speed):
		self.bodyFrameNo.inc()
		self.kneeling = False
		self.movement.verticalMove(speed > 0)
		if speed != 0:
			self.xPos += speed
			self.vector = True if speed > 0 else False


	def stop(self):
		self.bodyFrameNo.current = 0
		self.movement.stop()


	def getHeadCoord(self):
		if self.kneeling:
			x = self.xPos + (105 if self.vector else -15)
			y = self.yPos + 110
		else:
			x = self.xPos + (60 if self.vector else 25)
			y = self.yPos - 30
		return (x,y)



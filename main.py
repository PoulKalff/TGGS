#!/usr/bin/python3

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import io
import os
import sys
import math
import time
import json
import pygame
import random
import requests
import argparse
import pygame.locals
from io import BytesIO
#from PIL import Image

from helperFunctions import *
from player import Player
from level import Level

# --- Variables / Ressources ----------------------------------------------------------------------

pygame.init()
version = '0.20'		# player animation complete
sounds = {}
#backgroundMusic = pygame.mixer.Sound("snd/Mozart.-.Symphony.No.40.1st.Movement.mp3")
#backgroundMusic.set_volume(0.03)
font30 = pygame.font.Font('freesansbold.ttf', 30)
font60 = pygame.font.Font('freesansbold.ttf', 60)


# --- Classes -------------------------------------------------------------------------------------

class Main():
	""" get data from API and display it """

	def __init__(self):
		self.width = 1280
		self.height = 720
		self.time_down = 0.0
		self.time_elapsed = 0.0
		self.develop = False
		pygame.init()
		pygame.display.set_caption('The Smulle Game')
		self.display = pygame.display.set_mode((self.width, self.height))
		self.renderList = []				# list of all objects to render for each frame


	def run(self):
		self.initGame()
		self.loop()


	def initGame(self):
		self.running = True
		self.player = Player(self)
		self.level = Level(self, 1)
		self.level.xPosition = self.player.xPos


	def checkInput(self):
		""" Checks and responds to input from keyboard and mouse """
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			# --- Key Down Events ---------------------------------------------
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					if self.player.yPos == self.player.yPosLevel:
						self.player.goingUp = True
				elif event.key == pygame.K_DOWN:
					if self.player.onGround():
						self.player.kneeling = True
			# --- Key Up Events -----------------------------------------------
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					self.running = False
				elif event.key == pygame.K_UP:
					self.player.goingUp = False
				elif event.key == pygame.K_DOWN:
					self.player.kneeling = False
				elif event.key == pygame.K_q:
					self.running = False
				elif event.key == pygame.K_SPACE:
					pass
		keysPressed = pygame.key.get_pressed()
		# --- FOR DEV ------------------------------------------------------
		if keysPressed[pygame.K_k]:					# kill player
			self.player.death = 1
		if keysPressed[pygame.K_d]:					# developer mode, disables collision
			self.develop = True
		if keysPressed[pygame.K_s]:					# stop all objects
			for o in self.level.visibleObjects:
				o.speed = 0
		# --- FOR DEV ------------------------------------------------------
		elif keysPressed[pygame.K_LEFT]:
			# move player
			if self.player.xPos > self.player.xPosMin:
				self.player.move(-10)
			elif self.level.xPos == 0 and self.player.xPos > 0:
				self.player.move(-10)
			elif self.level.xPos == 0 and self.player.xPos == 0:
				self.player.stop()
			else:
				self.player.move(0)
			# move level
			if self.level.xPos > 0 and self.player.xPos == self.player.xPosMin:
				self.level.move(-10)
		elif keysPressed[pygame.K_RIGHT]:
			# move player
			if self.player.xPos < self.player.xPosMax:
				self.player.move(10)
			elif self.level.xPos == self.level.xPosMax and self.player.xPos < self.width:
				self.player.move(10)
			elif self.level.xPos == self.level.xPosMax and self.player.xPos == self.player.xPosMax:
				self.player.stop()
			else:
				self.player.move(0)
			# move level
			if self.level.xPos < self.level.xPosMax and self.player.xPos == self.player.xPosMax:
				self.level.move(10)
			# check complete
			if self.player.xPos >= self.width:
				self.level.triggerEnd()
		elif self.player.movement.isMoving() and not self.player.goingUp and self.player.yPos == self.player.yPosLevel:
			self.player.stop()



	def checkCollision(self):
		""" check if player's gfx overlaps any enemy's gfx """
		if self.player.death or self.develop:
			return 0
		xPosHead, yPosHead = self.player.getHeadCoord()
		for obj in self.level.visibleObjects:
			if obj.collisionType:
				objXPos = self.width - (self.level.xPos + self.width - obj.xPos)		# calculate obj posistion on screen, obj.xPos is position on level
				offset1 = (objXPos - self.player.xPos, obj.yPos - self.player.yPos)		# body
				offset2 = (objXPos - xPosHead, obj.yPos - yPosHead)						# head
				overlap1 = self.player.bodyMask.overlap(obj.mask, offset1)
				overlap2 = self.player.headMask.overlap(obj.mask, offset2)
				if overlap1 or overlap2:
					self.player.death = 1
		return 1




	def loop(self):
		""" Ensure that view runs until terminated by user """
		while self.running:
			self.checkInput()
			self.level.update()
			self.player.update()
			self.checkCollision()
			self.renderList.sort(key=lambda x: x.priority)
			for obj in self.renderList:
				self.display.blit(obj.frame, obj.coordinate)
			pygame.display.update()
			self.renderList = []
		pygame.quit()
		print('\n  Game terminated gracefully')


# --- Main  ---------------------------------------------------------------------------------------


#check arguments
parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=120))
parser.add_argument("-v", "--version",	action="store_true",	help="Print version and exit")
args = parser.parse_args()


colors = colorList
obj =  Main()
obj.run()


# --- TODO ---------------------------------------------------------------------------------------
# - enemies move more advanced, eg jump, move back/forth, change speed
# - vaaben/skud?
# - sounds on objects

# - ting man kan hoppe op på, eks. toadstool


# --- NOTES --------------------------------------------------------------------------------------







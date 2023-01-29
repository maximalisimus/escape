#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import pathlib
from typing import Tuple
from enum import Enum
import time

FPS = 60
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
infoObject = pygame.display.Info()
w = infoObject.current_w
h = infoObject.current_h
display1 = pygame.display.set_mode((w , h))
pygame.display.set_caption("Test")
#pygame.display.set_icon(pygame.image.load(str(pathlib.Path('./config/').joinpath('logo.png').resolve())))

current_scene = None
clock = pygame.time.Clock()
running = True

from tmainmenu import *

def SwitchScene(scene):
	global current_scene
	current_scene = scene

def info():
	print('Info')

def work():
	global display1, clock, running, w, h
		
	display1.fill((64, 64, 64))
	pygame.display.update()
		
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				SwitchScene(None)
			#elif event.type == STOPPED_PLAYING:
				# pass
			elif event.type == pygame.KEYDOWN:
				# if event.key == pygame.K_F2:
				#	pass
				pass
			elif event.type == pygame.KEYUP:
				# if event.key in []:
				pass
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pass
			elif  event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				pass
			elif event.type == pygame.MOUSEMOTION:
				pass
		
		#keys = pygame.key.get_pressed()
		# if keys[pygame.K_SPACE]:
		#	pass
		#pressed = pygame.mouse.get_pressed()
		#if pressed[0]:
		#	pos = pygame.mouse.get_pos()
		#	print(pos)
				
		clock.tick(FPS)

def main():
	SwitchScene(work)
	while current_scene is not None:
		current_scene()

if __name__ == '__main__':
	main()

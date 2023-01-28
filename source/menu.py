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
	
	up_menu_text = ('Игра', 'Помощь')
	main_menu = TMenu(up_menu_text)
	
	sub_menu_param_1 = (TypeMenu.Menu, False, 'Сначала', 'F2', info)
	sub_menu_param_2 = (TypeMenu.Menu, True, 'Перерыв', 'F3', info)
	sub_menu_param_3 = (TypeMenu.Menu, False, 'Лучшие игроки', 'F5', info)
	sub_menu_param_4 = (TypeMenu.Menu, True, 'Музыка', 'F6', info)
	sub_menu_param_5 = (TypeMenu.Menu, True, 'Звук', 'F7', info)
	sub_menu_param_6 = (TypeMenu.Sep, False, '', '', info)
	sub_menu_param_7 = (TypeMenu.Menu, False, 'Выход', 'F4', info)
	sub_menu_param_8 = (TypeMenu.Menu, False, 'О программе', 'F8', info)
	
	#sub_menu1 = TSub(main_menu.menu.sprites()[0].rect, True)
	#sub_menu1.add(*sub_menu_param_1)
	#sub_menu1.add(*sub_menu_param_2)
	#sub_menu1.add(*sub_menu_param_3)
	#sub_menu1.add(*sub_menu_param_4)
	#sub_menu1.add(*sub_menu_param_5)
	#sub_menu1.add(*sub_menu_param_6)
	#sub_menu1.add(*sub_menu_param_7)
	#sub_menu1.build()
	#sub_menu1.menu.sprites()[0].ismenu = True
	#sub_menu1.menu.sprites()[2].ismenu = True
	#sub_menu1.menu.sprites()[4].ismenu = True
	#sub_menu1.menu.sprites()[-1].ismenu = True
	#sub_menu1.draw(display1)
	#pygame.display.update()
	
	#sub_menu2 = TSub(main_menu.menu.sprites()[1].rect, False)
	#sub_menu2.add(*sub_menu_param_8)
	#sub_menu2.build()
	#sub_menu2.menu.sprites()[0].ismenu = True
	#sub_menu2.draw(display1)
	#pygame.display.update()
	
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
				main_menu.updateclick(event.pos)
			elif  event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				pass
			elif event.type == pygame.MOUSEMOTION:
				main_menu.update(event.pos)
		
		#keys = pygame.key.get_pressed()
		# if keys[pygame.K_SPACE]:
		#	pass
		#pressed = pygame.mouse.get_pressed()
		#if pressed[0]:
		#	pos = pygame.mouse.get_pos()
		#	print(pos)
		
		main_menu.draw(display1)
		pygame.display.update()
		
		clock.tick(FPS)

def main():
	SwitchScene(work)
	while current_scene is not None:
		current_scene()

if __name__ == '__main__':
	main()

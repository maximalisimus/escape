#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from myfunc import *
import sys

def main():
	global screen1
	global clock
	
	global surf_table
	global rect_table
	
	global coord_score_bg
	global score_bg
	
	# Groups
	global blocks
	
	global logo	
	surf_start_bg = pygame.transform.scale(LoadSurf(logo), (W, H))
	screen1.blit(surf_start_bg, (0, 0))
	pygame.display.update()
	del surf_start_bg, logo
	
	RUN = True
	
	### Debug
	SwitchInitImage(screen1)
	#Restart(screen1)
	global helicopter
	onlevel = 1
	BuildLevel(surf_table, blocks, onlevel)
	DrawTotal(score_bg, 0, onlevel, 4, False)
	screen1.blit(surf_table, rect_table)
	screen1.blit(score_bg, (coord_score_bg[0], coord_score_bg[1]))
	if 'helicopter' in dir(sys.modules['builtins']):
		helicopter.draw(screen1)
		#helicopter.isAnim = True
	pygame.display.update()
	### Debug
	
	while RUN:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				RUN = False
				exit()
			elif event.type == pygame.KEYDOWN:
				# event.key
				pass
			elif event.type == pygame.KEYUP:
				# if event.key in []:
				pass
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if isStart:
					SwitchInitImage(screen1)
				elif isGame:
					pass
			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				pass
		
		#keys = pygame.key.get_pressed()
		#pressed = pygame.mouse.get_pressed()
		#if pressed[0]:
		#	pos = pygame.mouse.get_pos()
		#	print(pos)
				
		clock.tick(FPS)

if __name__ == '__main__':
	main()

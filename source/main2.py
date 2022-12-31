#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from myfunc import *

def main():
	global screen1
	global clock
	
	global surf_table
	global rect_table
	
	# Groups
	global blocks
	
	global logo	
	surf_start_bg = pygame.transform.scale(LoadSurf(logo), (W, H))
	screen1.blit(surf_start_bg, (0, 0))
	pygame.display.update()
	del surf_start_bg, logo
	
	RUN = True
	
	# Debug
	SwitchInitImage(screen1)
	#Restart(screen1)
	onlevel = 1
	BuildLevel(surf_table, blocks, onlevel)
	#screen1.blit(surf_table, rect_table)
	pygame.display.update()
	#helicopter.isAnim = True
			
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
		
		screen1.blit(surf_table, rect_table)
		#screen1.blit(helicopter.image, helicopter.rect)
		pygame.display.update()
		#helicopter.update()
		
		clock.tick(FPS)

if __name__ == '__main__':
	main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from myfunc import *

surf_start_bg = pygame.transform.scale(LoadSurf(logo), (W, H))

def main():
	global screen1
	global clock
	
	global surf_start_bg
	screen1.blit(surf_start_bg, (0, 0))
	pygame.display.update()
	del surf_start_bg
	
	RUN = True
	
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
		
		clock.tick(FPS)

if __name__ == '__main__':
	main()

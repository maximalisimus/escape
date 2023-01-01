#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from funcmy import *

def main():
	global screen1
	global clock
	
	global surf_table
	global rect_table
	global surf_bonus
	global rect_bonus
	
	global coord_score_bg
	global score_bg
	
	# Groups
	global blocks
	global bonus_blocks
	
	global logo	
	surf_start_bg = pygame.transform.scale(LoadSurf(logo), (W, H))
	screen1.blit(surf_start_bg, (0, 0))
	pygame.display.update()
	del surf_start_bg, logo
	
	RUN = True
	
	### Debug
	SwitchInitImage(screen1)
	#Restart(screen1)
	onlevel = 1
	if onlevel == 30:
		helicopter = Helicopter()
		BuildLevel(surf_table, blocks, onlevel, helicopter)
	else:
		BuildLevel(surf_table, blocks, onlevel)
	DrawTotal(score_bg, 0, onlevel, 4, False)
	screen1.blit(surf_table, rect_table)	
	screen1.blit(score_bg, (coord_score_bg[0], coord_score_bg[1]))
	if onlevel == 30:
		helicopter.draw(screen1)
		#helicopter.isAnim = True
	pygame.display.update()
	
	#CreateBonus(onlevel)
	#for i in range(5):
	#	CreateBonus(onlevel)
	#DrawBonus(surf_bonus)
	#for item in bonus_blocks:
	#	surf_bonus.blit(SearchSurf(all_bonuses, item.name), item.rect)
	#screen1.blit(surf_bonus, rect_bonus)
	#pygame.display.update()
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

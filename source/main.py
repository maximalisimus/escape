#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import pathlib
from typing import Tuple

pygame.init()

W, H = 596, 385
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Esc")
pygame.display.set_icon(pygame.image.load(str(pathlib.Path('./config/').joinpath('logo.png').resolve())))

clock = pygame.time.Clock()
FPS = 60

Score = Old_Score = 0
Level = Old_Level = 1
Live = Old_Live = 4

is_Start = True

images = {
		'bonus': {
					1: {
						'name': 'alarm',
						'surf': pygame.image.load(str(pathlib.Path('./images/alarm.png').resolve())).convert_alpha(),
						'score': 100,
						'type': 'bonus',
						},
					2: {
						'name': 'burger',
						'surf': pygame.image.load(str(pathlib.Path('./images/burger.png').resolve())).convert_alpha(),
						'score': 50,
						'type': 'bonus',
						},
					3: {
						'name': 'clock',
						'surf': pygame.image.load(str(pathlib.Path('./images/clock.png').resolve())).convert_alpha(),
						'score': 30,
						'type': 'bonus',
						},
					4: {
						'name': 'coffee',
						'surf': pygame.image.load(str(pathlib.Path('./images/coffee.png').resolve())).convert_alpha(),
						'score': 20,
						'type': 'bonus',
						},
					5: {
						'name': 'cola',
						'surf': pygame.image.load(str(pathlib.Path('./images/cola.png').resolve())).convert_alpha(),
						'score': 10,
						'type': 'bonus',
						},
					6: {
						'name': 'medicine_chest',
						'surf': pygame.image.load(str(pathlib.Path('./images/medicine-chest.png').resolve())).convert_alpha(),
						'score': 1,
						'type': 'bonus',
						},
					7: {
						'name': 'stop',
						'surf': pygame.image.load(str(pathlib.Path('./images/stop.png').resolve())).convert_alpha(),
						'score': 1,
						'type': 'bonus',
						},
					8: {
						'name': 'thermos',
						'surf': pygame.image.load(str(pathlib.Path('./images/thermos.png').resolve())).convert_alpha(),
						'score': 1,
						'type': 'bonus',
						},
					9: {
						'name': 'heart',
						'surf': pygame.image.load(str(pathlib.Path('./images/heart.png').resolve())).convert_alpha(),
						'score': 1,
						'type': 'bonus',
						},
				},
		'wall': {
				1: pygame.image.load(str(pathlib.Path('./images/tile-1.png').resolve())).convert_alpha(),
				2: pygame.image.load(str(pathlib.Path('./images/tile-2.png').resolve())).convert_alpha(),
				3: pygame.image.load(str(pathlib.Path('./images/tile-3.png').resolve())).convert_alpha(),
				4: pygame.image.load(str(pathlib.Path('./images/tile-4.png').resolve())).convert_alpha(),
				5: pygame.image.load(str(pathlib.Path('./images/tile-5.png').resolve())).convert_alpha(),
				6: pygame.image.load(str(pathlib.Path('./images/tile-6.png').resolve())).convert_alpha(),
				},
		'bg': {
				1: pygame.image.load(str(pathlib.Path('./images/esc_1.png').resolve())).convert_alpha(),
				2: pygame.image.load(str(pathlib.Path('./images/esc_2.png').resolve())).convert_alpha(),
				3: pygame.image.load(str(pathlib.Path('./images/esc_3.png').resolve())).convert_alpha(),
				4: pygame.image.load(str(pathlib.Path('./images/esc_4.png').resolve())).convert_alpha(),
				5: pygame.image.load(str(pathlib.Path('./images/esc_5.png').resolve())).convert_alpha(),
				6: pygame.image.load(str(pathlib.Path('./images/esc_6.png').resolve())).convert_alpha(),
				7: pygame.image.load(str(pathlib.Path('./images/esc_t.png').resolve())).convert_alpha(),
				8: pygame.image.load(str(pathlib.Path('./images/esc-bg.png').resolve())).convert_alpha(),
				9: pygame.image.load(str(pathlib.Path('./images/score-bg.png').resolve())).convert_alpha(),
			},
		'weapon': {
					1: { 
							'name': 'bomb',
							'surf': pygame.image.load(str(pathlib.Path('./images/bomb.png').resolve())).convert_alpha(),
							'type': 'weapon',
						},
					2: { 
							'name': 'shot',
							'surf': pygame.image.load(str(pathlib.Path('./images/bullet.png').resolve())).convert_alpha(),
							'type': 'weapon',
						},
				},
		'else': {
					1: pygame.image.load(str(pathlib.Path('./images/hatch-bombs.png').resolve())).convert_alpha(),
					2: pygame.image.load(str(pathlib.Path('./images/hatch-bombs-2.png').resolve())).convert_alpha(),
					3: pygame.image.load(str(pathlib.Path('./images/Helicopter_1.png').resolve())).convert_alpha(),
					4: pygame.image.load(str(pathlib.Path('./images/Helicopter_2.png').resolve())).convert_alpha(),
					5: pygame.image.load(str(pathlib.Path('./images/Helicopter_3.png').resolve())).convert_alpha(),
					6: pygame.image.load(str(pathlib.Path('./images/Helicopter_4.png').resolve())).convert_alpha(),
					7: pygame.image.load(str(pathlib.Path('./images/ladder.png').resolve())).convert_alpha(),
					8: pygame.image.load(str(pathlib.Path('./images/ladder-2.png').resolve())).convert_alpha(),
					9: pygame.image.load(str(pathlib.Path('./images/left-pistol.png').resolve())).convert_alpha(),
					10: pygame.image.load(str(pathlib.Path('./images/right-pistol.png').resolve())).convert_alpha(),
					11: pygame.image.load(str(pathlib.Path('./images/live-bg.png').resolve())).convert_alpha(),
					12: pygame.image.load(str(pathlib.Path('./images/died-bg.png').resolve())).convert_alpha(),
					13: pygame.image.load(str(pathlib.Path('./images/door.png').resolve())).convert_alpha(),
					14: pygame.image.load(str(pathlib.Path('./images/blade-rear.png').resolve())).convert_alpha(),
					15: pygame.image.load(str(pathlib.Path('./images/blade-up.png').resolve())).convert_alpha(),
				},
		'LCD': {
					'0': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-0.png').resolve())).convert_alpha(),
					'1': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-1.png').resolve())).convert_alpha(),
					'2': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-2.png').resolve())).convert_alpha(),
					'3': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-3.png').resolve())).convert_alpha(),
					'4': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-4.png').resolve())).convert_alpha(),
					'5': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-5.png').resolve())).convert_alpha(),
					'6': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-6.png').resolve())).convert_alpha(),
					'7': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-7.png').resolve())).convert_alpha(),
					'8': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-8.png').resolve())).convert_alpha(),
					'9': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-9.png').resolve())).convert_alpha(),
				},
		}

levels = map(lambda x: str(pathlib.Path('./levels/').joinpath(f"ESC_{x}.DAT").resolve()), range(1,31))

musics = str(pathlib.Path('./sounds/music.mp3').resolve())

sounds = {
			'alarm': str(pathlib.Path('./sounds/alarm.WAV').resolve()),
			'applause': str(pathlib.Path('./sounds/applause.WAV').resolve()),
			'bomb': str(pathlib.Path('./sounds/bomb.WAV').resolve()),
			'burger': str(pathlib.Path('./sounds/burger.WAV').resolve()),
			'clock': str(pathlib.Path('./sounds/clock.WAV').resolve()),
			'coffee': str(pathlib.Path('./sounds/coffee.WAV').resolve()),
			'cola': str(pathlib.Path('./sounds/cola.WAV').resolve()),
			'heart': str(pathlib.Path('./sounds/heart.WAV').resolve()),
			'jump': str(pathlib.Path('./sounds/jump.WAV').resolve()),
			'live': str(pathlib.Path('./sounds/live.WAV').resolve()),
			'final': str(pathlib.Path('./sounds/final.WAV').resolve()),
			'shot': str(pathlib.Path('./sounds/shot.WAV').resolve()),
			'start': str(pathlib.Path('./sounds/start.WAV').resolve()),
			'stop': str(pathlib.Path('./sounds/stop.WAV').resolve()),
			'thermos': str(pathlib.Path('./sounds/thermos.WAV').resolve())
		}

def print_level(level: int) -> str:
	if level<10:
		return f"0{level}"
	else:
		return f"{level}"

def print_score(score: int) -> str:
	if score < 10:
		return f"000000{score}"
	elif score < 100:
		return f"00000{score}"
	elif score < 1000:
		return f"0000{score}"
	elif score < 10000:
		return f"000{score}"
	elif score < 100000:
		return f"00{score}"
	elif score < 1000000:
		return f"0{score}"
	else:
		return f"{score}"

def DrawScore(surf, on_score: int):
	pygame.draw.rect(surf, (0,0,0), (475,40, 92, 22))
	OnScore = tuple(print_score(on_score))
	surf.blit(images['LCD'][OnScore[0]], (476, 41.5))
	surf.blit(images['LCD'][OnScore[1]], (489, 41.5))
	surf.blit(images['LCD'][OnScore[2]], (502, 41.5))
	surf.blit(images['LCD'][OnScore[3]], (515, 41.5))
	surf.blit(images['LCD'][OnScore[4]], (528, 41.5))
	surf.blit(images['LCD'][OnScore[5]], (541, 41.5))
	surf.blit(images['LCD'][OnScore[6]], (554, 41.5))

def DrawLevel(surf, on_level: int):
	pygame.draw.rect(surf, (0,0,0), (510, 111, 26, 22))
	OnLevel = tuple(print_level(on_level))
	surf.blit(images['LCD'][OnLevel[0]], (511, 111))
	surf.blit(images['LCD'][OnLevel[1]], (524, 111))

def DrawTotal(surface, score: int, level: int, live: int):
	global Old_Score
	global Old_Level
	global Old_Live
	global is_Start
	
	if score != Old_Score:
		DrawScore(surface, score)
		Old_Score = score
	
	if level != Old_Level:
		DrawLevel(surface, level)
		Old_Level = level
	
	if live != Old_Live:
		Old_Live = live
		pass
	
	if is_Start:
		is_Start = False
		DrawScore(surface, score)
		Old_Score = score
		DrawLevel(surface, level)
		Old_Level = level

def main():
	
	global sc
	global clock
	global FPS
	
	sc.blit(images['bg'][8], (0, 0))
	sc.blit(images['bg'][9], (450, 0))
	
	
	### Copy Surface Variant
	DrawTotal(sc, 0, 1, 4)	
	# screen = pygame.Surface.copy(sc)
	# DrawTotal(screen, 0, 1, 4)
	# sc.blit(screen, (0, 0))
	### Copy Surface Variant
	
	surf_lives = pygame.Surface((128,32))
	surf_lives.blit(images['else'][11], (0,0))
	surf_lives.blit(images['else'][11], (32,0))
	surf_lives.blit(images['else'][11], (64,0))
	surf_lives.blit(images['else'][11], (96,0))
	sc.blit(surf_lives, (460, 160))
	
	#level_fonts = pygame.font.Font(str(pathlib.Path('./config/').joinpath('esc-lcd.ttf').resolve()), 35, bold=True, italic=False)
	#score_fonts = pygame.font.Font(str(pathlib.Path('./config/').joinpath('esc-lcd.ttf').resolve()), 38, bold=True, italic=False)
	
	#SCORE_COLOR = (192, 192, 192)
	#SCORE_BG = (0, 0, 0)
	
	#text_level = level_fonts.render('00', 1, SCORE_COLOR)
	#pos_level = text_level.get_rect(center=(525, 130))
	
	#text_score = score_fonts.render(print_score(0), 1, SCORE_COLOR)
	#pos_score = text_level.get_rect(center=(492, 59))
	
	#sc.blit(text_level, pos_level)
	#sc.blit(text_score, pos_score)
	
	#CHANGE_LEVEL = pygame.USEREVENT + 1
	#pygame.time.set_timer(CHANGE_LEVEL, 500)
		
	#x = 0
	
	pygame.display.update()
	
	RUN = True
	while RUN:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				RUN = False
				exit()
			#elif event.type == CHANGE_LEVEL:
			#	if x == 31:
			#		x = 0
			#	text_level = level_fonts.render(print_level(x), 1, SCORE_COLOR)
			#	sc.blit(bg, (0, 0))
			#	sc.blit(text_level, pos_level)
			#				
			#	text_score = score_fonts.render(print_score(x), 1, SCORE_COLOR)
			#	
			#	sc.blit(text_score, pos_score)
			#	
			#	x += 1
		
		#pygame.display.update()
		
		clock.tick(FPS)

if __name__ == '__main__':
	main()
